#!/usr/bin/env python3
"""
Train ML Model for Win Probability Prediction

This script:
1. Loads match history and player statistics from MongoDB
2. Prepares training data with engineered features
3. Trains a RandomForest classifier
4. Evaluates model performance
5. Saves the trained model and scaler
6. Updates MLModel in database with metrics

Usage:
    python scripts/train_model.py

Requirements:
    - scikit-learn
    - numpy
    - pandas (optional)
    - Django with configured settings
"""

import os
import sys
import pickle
import logging
from datetime import datetime
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from apps.matches.models import Match
from apps.users.models import UserStatistics
from apps.ml.models import MLModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WinProbabilityModelTrainer:
    """Trainer for win probability prediction model."""
    
    def __init__(self, model_type='random_forest', test_size=0.2, random_state=42):
        """Initialize trainer.
        
        Args:
            model_type: 'random_forest' or 'logistic_regression'
            test_size: Fraction of data to use for testing
            random_state: Random seed for reproducibility
        """
        self.model_type = model_type
        self.test_size = test_size
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.features_names = [
            'p1_total_matches', 'p1_wins', 'p1_losses', 'p1_draws', 'p1_win_rate',
            'p1_goals_for', 'p1_goals_against', 'p1_goal_diff', 'p1_clean_sheets',
            'p1_points', 'p1_ranking',
            'p2_total_matches', 'p2_wins', 'p2_losses', 'p2_draws', 'p2_win_rate',
            'p2_goals_for', 'p2_goals_against', 'p2_goal_diff', 'p2_clean_sheets',
            'p2_points', 'p2_ranking',
        ]
        self.metrics = {}
    
    def load_training_data(self, min_matches=5):
        """Load completed matches from database.
        
        Args:
            min_matches: Minimum matches per player to include in training
            
        Returns:
            (X, y) - Feature matrix and target vector
        """
        logger.info("Loading training data from database...")
        
        # Get all completed matches
        matches = Match.objects(status='completed', winner_id__ne=None).select_related()
        logger.info(f"Found {matches.count()} completed matches")
        
        if matches.count() == 0:
            logger.error("No completed matches found in database!")
            return None, None
        
        X = []
        y = []
        skipped = 0
        
        for match in matches:
            try:
                # Get player statistics
                stats1 = UserStatistics.objects(user_id=match.player1_id).first()
                stats2 = UserStatistics.objects(user_id=match.player2_id).first()
                
                if not stats1 or not stats2:
                    skipped += 1
                    continue
                
                # Skip if players have too few matches
                if stats1.total_matches < min_matches or stats2.total_matches < min_matches:
                    skipped += 1
                    continue
                
                # Extract features
                features = self._extract_features(stats1, stats2)
                
                # Determine label (1 if player1 won, 0 if player2 won)
                label = 1 if match.winner_id == match.player1_id else 0
                
                X.append(features)
                y.append(label)
                
            except Exception as e:
                logger.warning(f"Error processing match {match.match_id}: {str(e)}")
                skipped += 1
                continue
        
        logger.info(f"Loaded {len(X)} training samples ({skipped} skipped)")
        
        if len(X) < 10:
            logger.error("Not enough training data! Need at least 10 samples.")
            return None, None
        
        return np.array(X), np.array(y)
    
    def _extract_features(self, stats1, stats2):
        """Extract feature vector from two player statistics."""
        def get_player_features(stats):
            total_matches = stats.total_matches if stats.total_matches > 0 else 1
            win_rate = stats.match_wins / total_matches if total_matches > 0 else 0.0
            goal_difference = (stats.goals_scored - stats.goals_conceded) if (stats.goals_scored and stats.goals_conceded) else 0
            ranking = stats.ranking if stats.ranking else 999
            
            return [
                stats.total_matches,
                stats.match_wins,
                stats.match_losses,
                stats.match_draws,
                win_rate,
                stats.goals_scored or 0,
                stats.goals_conceded or 0,
                goal_difference,
                stats.clean_sheets or 0,
                stats.points or 0,
                ranking,
            ]
        
        p1_features = get_player_features(stats1)
        p2_features = get_player_features(stats2)
        
        # Concatenate features
        return p1_features + p2_features
    
    def prepare_data(self, X, y):
        """Split and scale data.
        
        Args:
            X: Feature matrix
            y: Target vector
        """
        logger.info("Preparing training data...")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        
        logger.info(f"Training set: {len(self.X_train)} samples")
        logger.info(f"Test set: {len(self.X_test)} samples")
        logger.info(f"Class distribution (train): {np.bincount(self.y_train)}")
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        logger.info("Data prepared and scaled")
    
    def train(self):
        """Train the model."""
        logger.info(f"Training {self.model_type} model...")
        
        if self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                n_jobs=-1,
                class_weight='balanced'
            )
        elif self.model_type == 'logistic_regression':
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=self.random_state,
                class_weight='balanced'
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        self.model.fit(self.X_train, self.y_train)
        logger.info("Model training completed")
    
    def evaluate(self):
        """Evaluate model performance."""
        logger.info("Evaluating model...")
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        # Probabilities
        y_train_proba = self.model.predict_proba(self.X_train)[:, 1]
        y_test_proba = self.model.predict_proba(self.X_test)[:, 1]
        
        # Metrics
        self.metrics = {
            'train_accuracy': float(accuracy_score(self.y_train, y_train_pred)),
            'test_accuracy': float(accuracy_score(self.y_test, y_test_pred)),
            'train_precision': float(precision_score(self.y_train, y_train_pred, zero_division=0)),
            'test_precision': float(precision_score(self.y_test, y_test_pred, zero_division=0)),
            'train_recall': float(recall_score(self.y_train, y_train_pred, zero_division=0)),
            'test_recall': float(recall_score(self.y_test, y_test_pred, zero_division=0)),
            'train_f1': float(f1_score(self.y_train, y_train_pred, zero_division=0)),
            'test_f1': float(f1_score(self.y_test, y_test_pred, zero_division=0)),
            'train_auc': float(roc_auc_score(self.y_train, y_train_proba)),
            'test_auc': float(roc_auc_score(self.y_test, y_test_proba)),
        }
        
        logger.info("\n" + "="*50)
        logger.info("MODEL PERFORMANCE METRICS")
        logger.info("="*50)
        logger.info(f"Train Accuracy: {self.metrics['train_accuracy']:.4f}")
        logger.info(f"Test Accuracy:  {self.metrics['test_accuracy']:.4f}")
        logger.info(f"Train Precision: {self.metrics['train_precision']:.4f}")
        logger.info(f"Test Precision:  {self.metrics['test_precision']:.4f}")
        logger.info(f"Train Recall: {self.metrics['train_recall']:.4f}")
        logger.info(f"Test Recall:  {self.metrics['test_recall']:.4f}")
        logger.info(f"Train F1-Score: {self.metrics['train_f1']:.4f}")
        logger.info(f"Test F1-Score:  {self.metrics['test_f1']:.4f}")
        logger.info(f"Train AUC: {self.metrics['train_auc']:.4f}")
        logger.info(f"Test AUC:  {self.metrics['test_auc']:.4f}")
        logger.info("="*50 + "\n")
        
        logger.info("Classification Report (Test Set):")
        logger.info("\n" + classification_report(self.y_test, y_test_pred))
        
        logger.info("Confusion Matrix (Test Set):")
        logger.info("\n" + str(confusion_matrix(self.y_test, y_test_pred)) + "\n")
    
    def save_model(self, output_dir='ml_models'):
        """Save model and scaler to disk.
        
        Args:
            output_dir: Directory to save model
            
        Returns:
            Path to saved model
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Get version number
        existing_models = MLModel.objects(model_name='win_probability_model')
        version = (existing_models.count() + 1)
        
        # Filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{output_dir}/win_prob_model_v{version}_{timestamp}.pkl'
        
        # Save model and scaler
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'features': self.features_names,
            'model_type': self.model_type,
            'version': version,
            'trained_at': datetime.now().isoformat(),
            'metrics': self.metrics,
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to: {filename}")
        return filename
    
    def register_in_database(self, model_path, should_activate=True):
        """Register model in database.
        
        Args:
            model_path: Path to saved model file
            should_activate: Whether to set this as active model
        """
        # Deactivate previous models
        if should_activate:
            MLModel.objects(is_active=True).update(is_active=False)
        
        # Get version
        existing = MLModel.objects(model_name='win_probability_model')
        version = existing.count() + 1
        
        # Create new model record
        ml_model = MLModel(
            model_name='win_probability_model',
            model_type=self.model_type,
            version=version,
            is_active=should_activate,
            accuracy={
                'train_accuracy': self.metrics.get('train_accuracy'),
                'test_accuracy': self.metrics.get('test_accuracy'),
            },
            metrics=self.metrics,
            training_samples=len(self.X_train),
            trained_at=datetime.now(),
            features_used=self.features_names,
            model_path=model_path,
            status='completed'
        )
        ml_model.save()
        
        logger.info(f"Model registered in database: {ml_model.model_id}")
        logger.info(f"Model active: {should_activate}")
        logger.info(f"Model version: {version}")
        
        return ml_model


def main():
    """Main training pipeline."""
    try:
        logger.info("="*50)
        logger.info("WIN PROBABILITY MODEL TRAINING")
        logger.info("="*50 + "\n")
        
        # Initialize trainer
        trainer = WinProbabilityModelTrainer(model_type='random_forest')
        
        # Load data
        X, y = trainer.load_training_data(min_matches=3)
        if X is None:
            logger.error("Failed to load training data")
            return False
        
        # Prepare data
        trainer.prepare_data(X, y)
        
        # Train model
        trainer.train()
        
        # Evaluate
        trainer.evaluate()
        
        # Save model
        model_path = trainer.save_model()
        
        # Register in database
        ml_model = trainer.register_in_database(model_path, should_activate=True)
        
        logger.info("\n" + "="*50)
        logger.info("TRAINING COMPLETED SUCCESSFULLY!")
        logger.info("="*50)
        logger.info(f"Model ID: {ml_model.model_id}")
        logger.info(f"Model Path: {model_path}")
        logger.info(f"Test Accuracy: {trainer.metrics['test_accuracy']:.4f}")
        logger.info(f"Test AUC: {trainer.metrics['test_auc']:.4f}")
        logger.info("="*50 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}", exc_info=True)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
