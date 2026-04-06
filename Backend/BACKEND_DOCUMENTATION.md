# 🏆 Football Tournament Backend - Complete Documentation

**Version:** 1.0.0  
**Last Updated:** March 30, 2026  
**Tech Stack:** Django 4.2 • DRF • MongoDB • Channels • scikit-learn • JWT

---

## Table of Contents

1. [📌 Project Overview](#project-overview)
2. [🏗️ Project Structure](#project-structure)
3. [🧠 Data Models](#data-models)
4. [🔐 Authentication System](#authentication-system)
5. [🌐 API Endpoints](#api-endpoints)
6. [⚡ Real-Time Features (WebSockets)](#real-time-features)
7. [📂 File Upload System](#file-upload-system)
8. [🧮 Business Logic](#business-logic)
9. [🔒 Security Features](#security-features)
10. [🤖 AI/ML System](#ai-ml-system)
11. [🚀 How to Run Backend Locally](#how-to-run-backend-locally)
12. [🔗 Integration Guide for Frontend](#integration-guide-for-frontend)
13. [📦 Sample API Flow](#sample-api-flow)
14. [🧪 Testing APIs](#testing-apis)
15. [📌 Notes & Future Improvements](#notes--future-improvements)

---

## 📌 Project Overview

### What This Backend Does

The Football Tournament Backend is a **complete tournament management and game analytics system** that handles:

- **User Management:** Registration, login, profile management, and statistics tracking
- **Tournament Management:** Create, join, manage tournaments with multiple formats (Knockout, League)
- **Match System:** Record match results with proof uploads, auto-winner detection, and event tracking
- **Auction System:** Real-time live player auctions with bidding during tournaments
- **Leaderboard System:** Dynamic rankings with Win=3, Draw=1, Loss=0 points system
- **Mission/Quests System:** Daily, weekly, seasonal quests with multi-currency rewards
- **Club Management:** Player clubs with membership roles and contribution tracking
- **Anti-Cheat System:** Report inappropriate behavior with admin review workflow
- **Real-Time Features:** WebSocket consumers for live match updates, auction bidding, and notifications
- **AI Predictions:** Machine learning model to predict match win probability
- **Analytics:** Player statistics, tournament analytics, and performance metrics

### Tech Stack Overview

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Django 4.2 | Web framework |
| **API** | Django REST Framework (DRF) | RESTful API |
| **Database** | MongoDB | NoSQL document database |
| **ODM** | Mongoengine | MongoDB document mapper |
| **Authentication** | JWT (SimpleJWT) | Token-based auth |
| **Real-Time** | Django Channels | WebSocket support |
| **Messaging** | Redis | Channel layer for WebSockets |
| **ML** | scikit-learn | Machine learning models |
| **Server** | Daphne | ASGI server for async |
| **Container** | Docker | Containerization & deployment |

### High-Level Architecture

```
┌─────────────────┬──────────────────┬─────────────────┐
│   Frontend      │   REST APIs      │   WebSockets    │
│   (React)       │   (DRF)          │   (Channels)    │
└────────┬────────┴────────┬─────────┴────────┬────────┘
         │                 │                  │
         └─────────────────┼──────────────────┘
                           │
                  ┌────────▼────────┐
                  │  Django ASGI    │
                  │  (Daphne)       │
                  └────────┬────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼─────┐    ┌─────▼─────┐
    │ MongoDB  │      │ Redis     │    │ ML Models │
    │ (Data)   │      │ (Cache &  │    │ (Predict) │
    │          │      │  Messages)│    │           │
    └──────────┘      └───────────┘    └───────────┘
```

---

## 🏗️ Project Structure

```
backend/
│
├── core/                          # Django core configuration
│   ├── settings.py               # Django settings & DB config
│   ├── urls.py                   # Main URL routing
│   ├── asgi.py                   # ASGI config for Channels
│   ├── wsgi.py                   # WSGI config for deployment
│   └── exceptions.py             # Custom exception handlers
│
├── apps/                          # Django applications (features)
│   │
│   ├── users/                    # User management & authentication
│   │   ├── models.py             # User, UserStatistics, UserBadge
│   │   ├── serializers.py        # Register, Login, Profile
│   │   ├── views.py              # Auth endpoints
│   │   ├── urls.py               # Auth routes
│   │   └── admin.py              # Django admin configuration
│   │
│   ├── tournaments/              # Tournament management
│   │   ├── models.py             # Tournament, TournamentPlayer
│   │   ├── serializers.py        # Tournament serializers
│   │   ├── views.py              # Tournament endpoints
│   │   ├── urls.py               # Tournament routes
│   │   └── admin.py
│   │
│   ├── matches/                  # Match management
│   │   ├── models.py             # Match, MatchEvent
│   │   ├── serializers.py        # Match serializers
│   │   ├── views.py              # Match endpoints (6 APIs)
│   │   ├── urls.py               # Match routes
│   │   └── admin.py
│   │
│   ├── auctions/                 # Auction system
│   │   ├── models.py             # Auction, AuctionBid
│   │   ├── serializers.py        # Auction serializers
│   │   ├── views.py              # Auction endpoints (7 APIs)
│   │   ├── urls.py               # Auction routes
│   │   └── admin.py
│   │
│   ├── leaderboard/              # Tournament leaderboard
│   │   ├── models.py             # Leaderboard, LeaderboardEntry
│   │   ├── serializers.py        # Leaderboard serializers
│   │   ├── views.py              # Leaderboard endpoints (6 APIs)
│   │   ├── urls.py               # Leaderboard routes
│   │   └── admin.py
│   │
│   ├── missions/                 # Quests & challenges
│   │   ├── models.py             # Mission, UserMission
│   │   ├── serializers.py        # Mission serializers
│   │   ├── views.py              # Mission endpoints (8 APIs)
│   │   ├── urls.py               # Mission routes
│   │   └── admin.py
│   │
│   ├── clubs/                    # Player clubs
│   │   ├── models.py             # Club, ClubMember
│   │   ├── serializers.py        # Club serializers
│   │   ├── views.py              # Club endpoints (9 APIs)
│   │   ├── urls.py               # Club routes
│   │   └── admin.py
│   │
│   ├── reports/                  # Anti-cheat reporting
│   │   ├── models.py             # Report
│   │   ├── serializers.py        # Report serializers
│   │   ├── views.py              # Report endpoints (7 APIs)
│   │   ├── urls.py               # Report routes
│   │   └── admin.py
│   │
│   ├── realtime/                 # WebSocket consumers
│   │   ├── consumers.py          # NotificationConsumer, MatchLiveConsumer, AuctionLiveConsumer
│   │   ├── routing.py            # WebSocket URL routing
│   │   ├── models.py
│   │   └── admin.py
│   │
│   └── ml/                       # Machine Learning
│       ├── models.py             # MLModel, PredictionCache
│       ├── predictor.py          # Win probability predictor
│       ├── serializers.py        # Prediction serializers
│       ├── views.py              # Prediction endpoints (3 APIs)
│       ├── urls.py               # ML routes
│       ├── admin.py
│       └── migrations/
│
├── scripts/                       # Utility scripts
│   └── train_model.py           # ML model training script
│
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image configuration
├── docker-compose.yml            # Docker services (MongoDB, Redis, Web)
├── .env.example                  # Environment variables template
├── manage.py                     # Django management CLI
└── BACKEND_DOCUMENTATION.md      # This file
```

### App-by-App Overview

| App | Purpose | Features | Endpoints |
|-----|---------|----------|-----------|
| `users` | Auth & profiles | Register, Login, Profile, Logout | 4+ |
| `tournaments` | Tournament management | Create, Join, Browse, Stats | 5+ |
| `matches` | Match recording | Submit result, Upload proof, Track events | 6 |
| `auctions` | Live player auctions | Start, Place bid, Track history | 7 |
| `leaderboard` | Rankings system | Generate ranks, Calculate points | 6 |
| `missions` | Quests system | Start mission, Update progress, Claim reward | 8 |
| `clubs` | Player clubs | Create, Join, Manage members | 9 |
| `reports` | Anti-cheat | Report, Admin review, Approve/Reject | 7 |
| `realtime` | WebSockets | Live updates, Notifications | 3 channels |
| `ml` | AI predictions | Predict winner probability | 3 |

---

## 🧠 Data Models

### Complete Database Schema

All models use **MongoDB** with unique IDs (UUIDs) and automatic timestamps.

---

### 👤 User Model

**Collection:** `users`

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "player_name",
  "email": "player@example.com",
  "password_hash": "hashed_password_string",
  "first_name": "John",
  "last_name": "Doe",
  "coins": 1000,
  "bio": "Professional footballer",
  "avatar_url": "https://storage.com/avatar.jpg",
  "phone_number": "+1234567890",
  "birth_date": "1990-05-15T00:00:00Z",
  "country": "USA",
  "stats": {
    "wins": 45,
    "losses": 12,
    "tournaments": 5,
    "rating": 2150
  },
  "is_verified": true,
  "is_premium": false,
  "is_active": true,
  "last_login": "2026-03-30T10:30:00Z",
  "created_at": "2026-01-15T08:00:00Z",
  "updated_at": "2026-03-30T10:30:00Z"
}
```

**Fields:**
- `user_id` - Unique UUID (auto-generated)
- `username` - 3-150 chars, alphanumeric + underscore/hyphen only
- `email` - Unique email address
- `password_hash` - Bcrypt hashed password (NEVER plain text)
- `coins` - In-game currency balance
- `stats` - JSON object with player statistics
- `is_verified` - Email verification status
- `is_premium` - Premium subscription status
- `created_at`, `updated_at` - Timestamps

---

### 📊 UserStatistics Model

**Collection:** `user_statistics`

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_tournaments": 5,
  "total_matches": 57,
  "match_wins": 45,
  "match_losses": 10,
  "match_draws": 2,
  "win_rate": 78.95,
  "goals_scored": 120,
  "goals_conceded": 45,
  "clean_sheets": 15,
  "points": 150,
  "ranking": 3,
  "updated_at": "2026-03-30T10:30:00Z"
}
```

**Auto-updated when:**
- Match completed
- Leaderboard recalculated
- Tournament finished

---

### 🏆 Tournament Model

**Collection:** `tournaments`

```json
{
  "tournament_id": "t-550e8400-e29b-41d4-a716-446655440000",
  "name": "Champions League 2026",
  "description": "Elite football tournament",
  "creator_id": "550e8400-e29b-41d4-a716-446655440000",
  "banner_image": "https://storage.com/banner.jpg",
  "start_date": "2026-04-01T10:00:00Z",
  "end_date": "2026-05-31T23:59:59Z",
  "format": "League",
  "max_players": 16,
  "current_players": 12,
  "status": "registration",
  "rules": "Best of 3 matches per round",
  "prize_pool": 10000,
  "location": "Virtual",
  "is_public": true,
  "created_at": "2026-03-15T10:00:00Z",
  "updated_at": "2026-03-30T10:30:00Z"
}
```

**Status Workflow:**
```
draft → registration → active → completed/cancelled
```

---

### ⚽ Match Model

**Collection:** `matches`

```json
{
  "match_id": "m-550e8400-e29b-41d4-a716-446655440000",
  "tournament_id": "t-550e8400-e29b-41d4-a716-446655440000",
  "player1_id": "550e8400-e29b-41d4-a716-446655440000",
  "player2_id": "550e8400-e29b-41d4-a716-446655440001",
  "player1_username": "Player1",
  "player2_username": "Player2",
  "match_date": "2026-03-30T15:00:00Z",
  "status": "completed",
  "score": {
    "player1": 3,
    "player2": 1
  },
  "winner_id": "550e8400-e29b-41d4-a716-446655440000",
  "loser_id": "550e8400-e29b-41d4-a716-446655440001",
  "proof_url": "https://storage.com/proof.mp4",
  "location": "Stadium A",
  "duration": 90,
  "created_at": "2026-03-30T08:00:00Z",
  "updated_at": "2026-03-30T17:00:00Z"
}
```

**Status Workflow:**
```
scheduled → live → completed/cancelled/disputed
```

---

### 💰 Auction Model

**Collection:** `auctions`

```json
{
  "auction_id": "a-550e8400-e29b-41d4-a716-446655440000",
  "tournament_id": "t-550e8400-e29b-41d4-a716-446655440000",
  "player_id": "550e8400-e29b-41d4-a716-446655440000",
  "player_username": "Ronaldo",
  "starting_bid": 5000,
  "current_bid": 12500,
  "highest_bidder_id": "550e8400-e29b-41d4-a716-446655440010",
  "highest_bidder_username": "TeamOwner1",
  "start_time": "2026-03-30T10:00:00Z",
  "end_time": "2026-03-30T12:00:00Z",
  "status": "sold",
  "player_rating": "5 stars",
  "total_bids": 24,
  "created_at": "2026-03-30T09:00:00Z",
  "updated_at": "2026-03-30T12:05:00Z"
}
```

**Bid Validation:**
- New bid must exceed current bid
- Minimum next bid = MAX(current_bid * 1.1, current_bid + 10)
- Bidder must have sufficient coins

---

### 🥇 Leaderboard Model

**Collection:** `leaderboard`

```json
{
  "leaderboard_id": "l-550e8400-e29b-41d4-a716-446655440000",
  "tournament_id": "t-550e8400-e29b-41d4-a716-446655440000",
  "entries": [
    {
      "position": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "Champion",
      "points": 30,
      "wins": 10,
      "losses": 0,
      "draws": 0,
      "goal_difference": 25,
      "win_rate": 100
    },
    {
      "position": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "username": "Runner-up",
      "points": 27,
      "wins": 9,
      "losses": 0,
      "draws": 0,
      "goal_difference": 18,
      "win_rate": 100
    }
  ],
  "updated_at": "2026-03-30T10:30:00Z"
}
```

**Points System:**
- Win = 3 points
- Draw = 1 point
- Loss = 0 points

**Tiebreaker Rules:** (in order)
1. Points (descending)
2. Goal Difference (descending)
3. Goals Scored (descending)

---

### 🎮 Mission Model

**Collection:** `missions`

```json
{
  "mission_id": "ms-550e8400-e29b-41d4-a716-446655440000",
  "title": "Win 5 Matches",
  "description": "Win 5 consecutive matches",
  "mission_type": "daily",
  "reward": {
    "coins": 500,
    "points": 100,
    "badge_id": "badge-bronze",
    "items": []
  },
  "condition": {
    "type": "wins",
    "value": 5
  },
  "difficulty": "medium",
  "status": "active",
  "start_date": "2026-03-30T00:00:00Z",
  "end_date": "2026-03-31T23:59:59Z",
  "created_at": "2026-03-25T10:00:00Z",
  "updated_at": "2026-03-30T10:30:00Z"
}
```

**Mission Types:**
- `daily` - Resets every 24 hours
- `weekly` - Resets every 7 days
- `seasonal` - Long-term (months)
- `special` - One-time events

---

### 👥 Club Model

**Collection:** `clubs`

```json
{
  "club_id": "c-550e8400-e29b-41d4-a716-446655440000",
  "name": "Real Madrid",
  "description": "Elite football club",
  "logo_url": "https://storage.com/logo.png",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000",
  "owner_username": "admin",
  "members": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001"
  ],
  "member_count": 2,
  "founded_date": "2026-03-01T10:00:00Z",
  "is_verified": false,
  "total_tournaments": 5,
  "total_wins": 15,
  "stats": {
    "wins": 15,
    "losses": 3,
    "points": 50
  },
  "created_at": "2026-03-01T10:00:00Z",
  "updated_at": "2026-03-30T10:30:00Z"
}
```

**Membership Roles:**
- `owner` - Club creator, can delete club, update info, cannot leave
- `admin` - Can manage members (invite/remove)
- `member` - Regular member

---

### 🚨 Report Model

**Collection:** `reports`

```json
{
  "report_id": "r-550e8400-e29b-41d4-a716-446655440000",
  "match_id": "m-550e8400-e29b-41d4-a716-446655440000",
  "reported_by_id": "550e8400-e29b-41d4-a716-446655440000",
  "reported_by_username": "Player1",
  "reported_player_id": "550e8400-e29b-41d4-a716-446655440001",
  "reason": "Suspicious score manipulation",
  "description": "Score jumped from 0-0 to 5-0 instantly",
  "proof_urls": [
    "https://storage.com/screenshot1.jpg",
    "https://storage.com/screenshot2.jpg"
  ],
  "status": "resolved",
  "severity": "high",
  "action_taken": "match_voided",
  "reviewed_by": "550e8400-e29b-41d4-a716-446655440999",
  "resolved_at": "2026-03-30T12:00:00Z",
  "resolution_notes": "Match voided due to evidence of cheating",
  "created_at": "2026-03-30T10:00:00Z",
  "updated_at": "2026-03-30T12:00:00Z"
}
```

**Status Workflow:**
```
pending → under_review → resolved/rejected
```

**Actions:**
- `match_voided` - Match result reversed
- `player_banned` - Player suspension
- `none` - No action (cleared)

---

### 🤖 ML Model Metadata

**Collection:** `ml_models`

```json
{
  "model_id": "ml-550e8400-e29b-41d4-a716-446655440000",
  "model_name": "win_probability_model",
  "model_type": "random_forest",
  "version": 1,
  "is_active": true,
  "accuracy": {
    "train_accuracy": 0.8945,
    "test_accuracy": 0.8723
  },
  "metrics": {
    "precision": 0.87,
    "recall": 0.86,
    "f1": 0.865,
    "auc": 0.92
  },
  "training_samples": 250,
  "trained_at": "2026-03-25T08:00:00Z",
  "features_used": ["total_matches", "wins", "losses", ...],
  "model_path": "/ml_models/win_prob_model_v1_20260325_080000.pkl",
  "status": "completed",
  "created_at": "2026-03-25T08:00:00Z",
  "updated_at": "2026-03-25T08:00:00Z"
}
```

---

## 🔐 Authentication System

### How JWT Authentication Works

This backend uses **JSON Web Tokens (JWT)** with SimpleJWT library.

#### Token Structure

```
access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTU... (short-lived)
refresh_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCJ... (long-lived)
```

**Token Lifetimes:**
- `access_token` - **15 minutes** (use for API calls)
- `refresh_token` - **7 days** (use to get new access tokens)

### Authentication Flow

#### 1. Register Flow

**Endpoint:** `POST /api/v1/auth/register/`

**Request:**
```json
{
  "username": "player_name",
  "email": "player@example.com",
  "password": "Secure@Pass123",
  "password_confirm": "Secure@Pass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 lowercase letter (a-z)
- At least 1 digit (0-9)

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "player_name",
    "email": "player@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "coins": 0,
    "is_verified": false,
    "is_premium": false,
    "created_at": "2026-03-30T10:00:00Z"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### 2. Login Flow

**Endpoint:** `POST /api/v1/auth/login/`

**Request:**
```json
{
  "username": "player_name",
  "password": "Secure@Pass123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "player_name",
    "email": "player@example.com",
    "coins": 1000,
    "is_verified": true,
    "last_login": "2026-03-30T10:30:00Z"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### 3. Token Usage in API Calls

**Add JWT to Request Headers:**

```javascript
// JavaScript fetch example
fetch('http://localhost:8000/api/v1/tournaments/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN_HERE',
    'Content-Type': 'application/json'
  }
})
```

**Header Format:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

#### 4. Refresh Token (Get New Access Token)

**Endpoint:** `POST /api/v1/auth/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**When to use:**
- When `access_token` expires (401 Unauthorized)
- Every 15 minutes proactively
- Keep `refresh_token` stored securely

---

#### 5. Logout Flow

**Endpoint:** `POST /api/v1/auth/logout/`

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

**Frontend Action:**
```javascript
// Clear stored tokens from localStorage/sessionStorage
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
```

---

## 🌐 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/
https://api.tournament.com/api/v1/  (production)
```

### Common Response Format

**Success Response (200-201):**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { },
  "timestamp": "2026-03-30T10:30:00Z"
}
```

**Error Response (400+):**
```json
{
  "success": false,
  "message": "Error message",
  "errors": { "field": ["Error detail"] },
  "timestamp": "2026-03-30T10:30:00Z"
}
```

**Status Codes:**
- `200` - OK (successful GET/POST)
- `201` - Created (resource created)
- `204` - No Content (successful DELETE)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (authentication needed)
- `403` - Forbidden (no permission)
- `404` - Not Found (resource doesn't exist)
- `500` - Server Error

---

### 🔓 Authentication APIs

#### Register User

- **URL:** `/auth/register/`
- **Method:** `POST`
- **Auth Required:** ❌ No
- **Request Body:**
  ```json
  {
    "username": "string (3-150 chars, unique)",
    "email": "string (unique email)",
    "password": "string (min 8 chars with uppercase, lowercase, digit)",
    "password_confirm": "string (must match password)",
    "first_name": "string (optional)",
    "last_name": "string (optional)"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "message": "User registered successfully",
    "user": { /* user object */ },
    "access": "string (jwt token)",
    "refresh": "string (jwt token)"
  }
  ```

---

#### Login User

- **URL:** `/auth/login/`
- **Method:** `POST`
- **Auth Required:** ❌ No
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "message": "Login successful",
    "user": { /* user object */ },
    "access": "string (jwt token)",
    "refresh": "string (jwt token)"
  }
  ```

---

#### Get User Profile

- **URL:** `/auth/profile/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes
- **Response:** `200 OK`
  ```json
  {
    "user_id": "string",
    "username": "string",
    "email": "string",
    "coins": "integer",
    "first_name": "string",
    "last_name": "string",
    "avatar_url": "string",
    "bio": "string",
    "is_verified": "boolean",
    "is_premium": "boolean",
    "created_at": "datetime"
  }
  ```

---

#### Update Profile

- **URL:** `/auth/profile/`
- **Method:** `PUT` / `PATCH`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "first_name": "string (optional)",
    "last_name": "string (optional)",
    "bio": "string (optional, max 500)",
    "avatar_url": "string (optional)",
    "phone_number": "string (optional)",
    "birth_date": "datetime (optional)"
  }
  ```
- **Response:** `200 OK` (updated user object)

---

#### Refresh Token

- **URL:** `/auth/token/refresh/`
- **Method:** `POST`
- **Auth Required:** ❌ No
- **Request Body:**
  ```json
  {
    "refresh": "string (refresh token)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "access": "string (new access token)"
  }
  ```

---

#### Logout

- **URL:** `/auth/logout/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "refresh": "string (refresh token)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "message": "Logout successful"
  }
  ```

---

### 🏆 Tournament APIs

#### Create Tournament

- **URL:** `/tournaments/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "name": "string (max 255)",
    "description": "string (optional, max 1000)",
    "start_date": "datetime",
    "end_date": "datetime",
    "format": "enum (Knockout | League)",
    "max_players": "integer (1-256)",
    "prize_pool": "integer (coins)",
    "rules": "string (optional)",
    "location": "string (optional)",
    "is_public": "boolean (default true)"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "tournament_id": "string",
    "name": "string",
    "creator_id": "string",
    "format": "string",
    "status": "draft",
    "current_players": 1,
    "max_players": "integer",
    "created_at": "datetime"
  }
  ```

---

#### Get All Tournaments

- **URL:** `/tournaments/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?status=active&format=League&search=Champions&page=1
  ```
- **Response:** `200 OK`
  ```json
  {
    "count": "integer",
    "next": "string (url)",
    "previous": "string (url)",
    "results": [
      {
        "tournament_id": "string",
        "name": "string",
        "format": "string",
        "status": "string",
        "current_players": "integer",
        "max_players": "integer",
        "start_date": "datetime",
        "created_at": "datetime"
      }
    ]
  }
  ```

---

#### Get Tournament Details

- **URL:** `/tournaments/{tournament_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (full tournament object)

---

#### Join Tournament

- **URL:** `/tournaments/{tournament_id}/join/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:** `{}` (empty)
- **Response:** `200 OK`
  ```json
  {
    "message": "Successfully joined tournament",
    "tournament_player": {
      "tournament_player_id": "string",
      "tournament_id": "string",
      "user_id": "string",
      "username": "string",
      "status": "active",
      "joined_at": "datetime"
    }
  }
  ```

---

#### Update Tournament Status

- **URL:** `/tournaments/{tournament_id}/update-status/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (creator only)
- **Request Body:**
  ```json
  {
    "status": "enum (registration | active | completed | cancelled)"
  }
  ```
- **Response:** `200 OK`

---

### ⚽ Match APIs (6 Endpoints)

#### Get Tournament Matches

- **URL:** `/matches/tournament/{tournament_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (list of matches)

---

#### Get Match Details

- **URL:** `/matches/{match_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (full match object)

---

#### Submit Match Result

- **URL:** `/matches/{match_id}/submit-result/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (match player only)
- **Request Body:**
  ```json
  {
    "player1_score": "integer",
    "player2_score": "integer",
    "proof": "file (jpg, png, gif, pdf, mp4, mov, max 10MB)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "match_id": "string",
    "winner_id": "string",
    "loser_id": "string",
    "is_draw": "boolean",
    "status": "completed"
  }
  ```

**Auto-Actions:**
- Auto-updates UserStatistics
- Auto-updates Leaderboard
- Sets winner based on score
- Detects draw if scores equal

---

#### Update Match Result

- **URL:** `/matches/{match_id}/update-result/`
- **Method:** `PUT`
- **Auth Required:** ✅ Yes (admin only)
- **Request Body:** (similar to submit)
- **Response:** `200 OK`

---

#### Get Player Stats

- **URL:** `/matches/player/{player_id}/stats/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "user_id": "string",
    "total_matches": "integer",
    "wins": "integer",
    "losses": "integer",
    "draws": "integer",
    "win_rate": "float (0-100)",
    "goals_scored": "integer",
    "goals_conceded": "integer"
  }
  ```

---

#### Get Player Matches

- **URL:** `/matches/player/{player_id}/matches/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?status=completed&limit=10
  ```
- **Response:** `200 OK` (list of player's matches)

---

### 💰 Auction APIs (7 Endpoints)

#### Start Auction

- **URL:** `/auctions/start/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (creator only)
- **Request Body:**
  ```json
  {
    "tournament_id": "string",
    "player_id": "string (auction player)",
    "starting_bid": "integer (coins)",
    "start_time": "datetime",
    "end_time": "datetime"
  }
  ```
- **Response:** `201 Created` (auction object)

---

#### Get Tournament Auctions

- **URL:** `/auctions/tournament/{tournament_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?status=live&sort=-current_bid
  ```
- **Response:** `200 OK` (list of auctions)

---

#### Get Active Auctions

- **URL:** `/auctions/active/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (live auctions only)

---

#### Get Auction Details

- **URL:** `/auctions/{auction_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "auction_id": "string",
    "player_username": "string",
    "current_bid": "integer",
    "highest_bidder": "string",
    "total_bids": "integer",
    "time_remaining": "string (HH:MM:SS)",
    "recent_bids": [
      {
        "bidder": "string",
        "amount": "integer",
        "time": "datetime"
      }
    ],
    "status": "string",
    "created_at": "datetime"
  }
  ```

---

#### Place Bid

- **URL:** `/auctions/{auction_id}/place-bid/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "bid_amount": "integer"
  }
  ```
- **Validations:**
  - Bid must be >= MIN_NEXT_BID (auto-calculated)
  - User must have sufficient coins
  - Auction must be live
  - User cannot be current highest bidder
- **Response:** `200 OK`
  ```json
  {
    "message": "Bid placed successfully",
    "current_highest": "integer",
    "min_next_bid": "integer",
    "your_position": "highest | outbid"
  }
  ```

**MIN_NEXT_BID Calculation:**
```
MIN_NEXT_BID = MAX(current_bid * 1.1, current_bid + 10)
```

---

#### Get Bid History

- **URL:** `/auctions/{auction_id}/bid-history/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (paginated bid history)

---

#### Get User Auction Stats

- **URL:** `/auctions/user/{user_id}/stats/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "total_bids": "integer",
    "auctions_won": "integer",
    "total_coins_spent": "integer",
    "average_bid": "float"
  }
  ```

---

### 🥇 Leaderboard APIs (6 Endpoints)

#### Get Tournament Leaderboard

- **URL:** `/leaderboard/tournament/{tournament_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "tournament_id": "string",
    "leaderboard": [
      {
        "rank": 1,
        "user_id": "string",
        "username": "string",
        "points": 30,
        "wins": 10,
        "losses": 0,
        "draws": 0,
        "goal_difference": 25,
        "win_rate": 100.0
      }
    ]
  }
  ```

---

#### Get Rankings

- **URL:** `/leaderboard/rankings/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?tournament_id=string&page=1&limit=20
  ```
- **Response:** `200 OK` (paginated rankings)

---

#### Get Top Players

- **URL:** `/leaderboard/top-players/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?limit=10&tournament_id=string
  ```
- **Response:** `200 OK` (top 10 players)

---

#### Get Player Leaderboard Stats

- **URL:** `/leaderboard/player/{player_id}/stats/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "user_id": "string",
    "rank": "integer",
    "points": "integer",
    "matches_played": "integer",
    "win_rate": "float",
    "tournaments_participated": "integer"
  }
  ```

---

#### Get My Rank

- **URL:** `/leaderboard/my-rank/{tournament_id}/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes
- **Response:** `200 OK` (current player's rank in tournament)

---

#### View Leaderboard Update

- **URL:** `/leaderboard/{tournament_id}/update/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (admin only)
- **Request Body:** `{}` (trigger recalculation)
- **Response:** `200 OK`

---

### 🎮 Mission APIs (8 Endpoints)

#### Get Available Missions

- **URL:** `/missions/available/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?mission_type=daily&difficulty=medium&status=active
  ```
- **Response:** `200 OK` (list of active missions)

---

#### Start Mission

- **URL:** `/missions/start/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "mission_id": "string"
  }
  ```
- **Validation:** Cannot start same mission twice
- **Response:** `201 Created`
  ```json
  {
    "user_mission_id": "string",
    "mission_title": "string",
    "progress": 0,
    "condition_value": "integer",
    "started_at": "datetime"
  }
  ```

---

#### Get User Missions

- **URL:** `/missions/my-missions/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes
- **Query Parameters:**
  ```
  ?status=active&include_completed=false
  ```
- **Response:** `200 OK`
  ```json
  {
    "active": [ /* incomplete missions */ ],
    "completed": [ /* completed missions */ ]
  }
  ```

---

#### Get Mission Details

- **URL:** `/missions/{mission_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (full mission object)

---

#### Update Mission Progress

- **URL:** `/missions/{user_mission_id}/update-progress/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (backend auto-updates, but exposed for testing)
- **Request Body:**
  ```json
  {
    "progress_value": "integer (amount to add)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "progress": "integer",
    "condition_value": "integer",
    "completed": "boolean",
    "message": "Mission updated / Mission completed!"
  }
  ```

---

#### Get Pending Rewards

- **URL:** `/missions/pending-rewards/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes
- **Response:** `200 OK`
  ```json
  {
    "pending_count": "integer",
    "rewards": [
      {
        "user_mission_id": "string",
        "mission_title": "string",
        "reward": { "coins": 500, "points": 100 }
      }
    ]
  }
  ```

---

#### Claim Reward

- **URL:** `/missions/{user_mission_id}/claim-reward/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Validation:** Mission must be completed and reward not claimed
- **Response:** `200 OK`
  ```json
  {
    "message": "Reward claimed successfully",
    "reward": { "coins": 500, "points": 100 },
    "new_balance": { "coins": 1500, "points": 250 }
  }
  ```

**Auto-Actions:**
- Adds coins to user account
- Adds points to leaderboard
- Awards badges if present
- Marks reward_claimed = true

---

#### Get Mission Stats

- **URL:** `/missions/stats/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes
- **Response:** `200 OK`
  ```json
  {
    "missions_started": "integer",
    "missions_completed": "integer",
    "total_coins_earned": "integer",
    "total_points_earned": "integer"
  }
  ```

---

### 👥 Club APIs (9 Endpoints)

#### Create Club

- **URL:** `/clubs/create/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "name": "string (3-255 chars, unique)",
    "description": "string (optional, max 1000)",
    "logo_url": "string (optional)"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "club_id": "string",
    "name": "string",
    "owner_id": "string (current user)",
    "member_count": 1,
    "created_at": "datetime"
  }
  ```

**Auto-Actions:**
- Creator automatically becomes owner
- ClubMember record created

---

#### Get All Clubs

- **URL:** `/clubs/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Query Parameters:**
  ```
  ?search=Real&is_verified=true&sort=-member_count
  ```
- **Response:** `200 OK` (paginated club list)

---

#### Get Club Details

- **URL:** `/clubs/{club_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "club_id": "string",
    "name": "string",
    "description": "string",
    "logo_url": "string",
    "owner_username": "string",
    "member_count": "integer",
    "is_verified": "boolean",
    "stats": { "wins": 15, "losses": 3 },
    "created_at": "datetime"
  }
  ```

---

#### Update Club Info

- **URL:** `/clubs/{club_id}/update/`
- **Method:** `PUT`
- **Auth Required:** ✅ Yes (owner only)
- **Request Body:**
  ```json
  {
    "description": "string (optional)",
    "logo_url": "string (optional)"
  }
  ```
- **Response:** `200 OK` (updated club object)

---

#### Join Club

- **URL:** `/clubs/{club_id}/join/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:** `{}` (empty)
- **Validation:** Cannot join same club twice
- **Response:** `200 OK`
  ```json
  {
    "message": "Successfully joined club",
    "club": { /* club object */ }
  }
  ```

**Auto-Actions:**
- Creates ClubMember record
- Adds user to club members list
- Increments member_count

---

#### Leave Club

- **URL:** `/clubs/{club_id}/leave/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (non-owner only)
- **Request Body:** `{}` (empty)
- **Validation:** Owner cannot leave
- **Response:** `200 OK`
  ```json
  {
    "message": "Successfully left club"
  }
  ```

---

#### Get User's Clubs

- **URL:** `/clubs/user/{user_id}/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK` (user's club memberships)

---

#### Get Club Stats

- **URL:** `/clubs/{club_id}/stats/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "member_count": "integer",
    "total_tournaments": "integer",
    "total_wins": "integer",
    "average_win_rate": "float",
    "most_active_member": "string"
  }
  ```

---

#### Get Club Members

- **URL:** `/clubs/{club_id}/members/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "members": [
      {
        "user_id": "string",
        "username": "string",
        "role": "owner | admin | member",
        "contribution_score": "integer",
        "joined_at": "datetime"
      }
    ]
  }
  ```

---

### 🚨 Report APIs (7 Endpoints)

#### Create Report

- **URL:** `/reports/create/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes
- **Request Body:**
  ```json
  {
    "match_id": "string",
    "reported_player_id": "string",
    "reason": "string (max 500)",
    "description": "string (optional, max 2000)",
    "severity": "enum (low | medium | high | critical)",
    "proof_files": "file array (optional, jpg/png/pdf/mp4, 10MB each)"
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "report_id": "string",
    "status": "pending",
    "created_at": "datetime"
  }
  ```

---

#### Get All Reports

- **URL:** `/reports/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes (admin only)
- **Query Parameters:**
  ```
  ?status=pending&severity=high&sort=-created_at
  ```
- **Response:** `200 OK` (paginated reports)

---

#### Get Report Details

- **URL:** `/reports/{report_id}/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes (admin or reporter)
- **Response:** `200 OK` (full report object with proof files)

---

#### Review Report

- **URL:** `/reports/{report_id}/review/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (admin only)
- **Request Body:** `{}` (empty, marks as under_review)
- **Response:** `200 OK`
  ```json
  {
    "status": "under_review",
    "reviewed_by": "admin_id",
    "reviewed_at": "datetime"
  }
  ```

---

#### Approve Report

- **URL:** `/reports/{report_id}/approve/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (admin only)
- **Request Body:**
  ```json
  {
    "action_taken": "enum (match_voided | player_banned | none)",
    "resolution_notes": "string (optional)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "status": "resolved",
    "action_taken": "string",
    "resolved_at": "datetime"
  }
  ```

**Actions Trigger:**
- `match_voided` → Match result reversed, players' stats reset
- `player_banned` → Player suspended, cannot join tournaments
- `none` → No action, case closed

---

#### Reject Report

- **URL:** `/reports/{report_id}/reject/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (admin only)
- **Request Body:**
  ```json
  {
    "resolution_notes": "string (reason for rejection)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "status": "rejected",
    "resolved_at": "datetime"
  }
  ```

---

#### Get Report Stats

- **URL:** `/reports/stats/`
- **Method:** `GET`
- **Auth Required:** ✅ Yes (admin only)
- **Response:** `200 OK`
  ```json
  {
    "total_reports": "integer",
    "pending": "integer",
    "under_review": "integer",
    "resolved": "integer",
    "rejected": "integer",
    "average_resolution_time": "string (HH:MM:SS)"
  }
  ```

---

### 🤖 ML/Prediction APIs (3 Endpoints)

#### Predict Match Winner

- **URL:** `/ml/predict/`
- **Method:** `POST`
- **Auth Required:** ❌ No
- **Request Body:**
  ```json
  {
    "player1_id": "string",
    "player2_id": "string",
    "use_cache": "boolean (default true)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "player1_id": "string",
    "player2_id": "string",
    "player1_win_probability": 0.65,
    "player2_win_probability": 0.35,
    "confidence": 0.82,
    "predicted_at": "datetime",
    "cached": false
  }
  ```

**How it Works:**
1. Extracts player statistics (matches, wins, losses, goals, etc.)
2. Calculates feature difference (relative strength)
3. Scales features using StandardScaler
4. Runs through trained RandomForest model
5. Returns probability both players winning
6. Caches result for 1 hour

**Confidence Score:** Based on number of matches played (higher = more reliable)

---

#### Get Model Statistics

- **URL:** `/ml/model-stats/`
- **Method:** `GET`
- **Auth Required:** ❌ No
- **Response:** `200 OK`
  ```json
  {
    "model_name": "win_probability_model",
    "model_type": "random_forest",
    "version": 1,
    "accuracy": {
      "train_accuracy": 0.8945,
      "test_accuracy": 0.8723
    },
    "metrics": {
      "precision": 0.87,
      "recall": 0.86,
      "f1": 0.865,
      "auc": 0.92
    },
    "training_samples": 250,
    "trained_at": "datetime",
    "is_active": true,
    "status": "completed"
  }
  ```

---

#### Reload Model

- **URL:** `/ml/reload-model/`
- **Method:** `POST`
- **Auth Required:** ✅ Yes (admin only)
- **Request Body:** `{}` (empty)
- **Response:** `200 OK`
  ```json
  {
    "message": "Model reloaded successfully"
  }
  ```

**When to Use:** After training a new model with training script

---

## ⚡ Real-Time Features (WebSockets)

### Overview

The backend uses **Django Channels** with **Redis** for real-time features.

| Feature | Channel | Purpose |
|---------|---------|---------|
| **Notifications** | `/ws/notifications/` | User-specific alerts |
| **Live Matches** | `/ws/matches/{match_id}/` | Match updates |
| **Auction Bidding** | `/ws/auctions/{auction_id}/` | Live bid updates |

---

### Connection URLs

```
Development:
ws://localhost:8000/ws/notifications/
ws://localhost:8000/ws/matches/{match_id}/
ws://localhost:8000/ws/auctions/{auction_id}/

Production (with SSL):
wss://api.tournament.com/ws/notifications/
wss://api.tournament.com/ws/matches/{match_id}/
wss://api.tournament.com/ws/auctions/{auction_id}/
```

---

### 🔔 Notifications Consumer

**URL:** `/ws/notifications/`

**Authentication:** Required (JWT token or authenticated session)

#### Connection Message

**To Client (on connect):**
```json
{
  "type": "connection_established",
  "status": "connected",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-03-30T10:30:00Z"
}
```

#### Client Messages

**Heartbeat (send every 30 seconds):**
```json
{
  "type": "heartbeat"
}
```

**Subscribe:**
```json
{
  "type": "subscribe"
}
```

#### Server Messages (Received from backend)

**Mission Completed:**
```json
{
  "type": "mission_completed",
  "mission_id": "string",
  "mission_name": "Win 5 Matches",
  "reward_coins": 500,
  "reward_points": 100,
  "timestamp": "2026-03-30T10:35:00Z"
}
```

**Auction Won:**
```json
{
  "type": "auction_won",
  "auction_id": "string",
  "player_name": "Ronaldo",
  "winning_bid": 12500,
  "tournament_id": "string",
  "timestamp": "2026-03-30T10:30:00Z"
}
```

**Club Invitation:**
```json
{
  "type": "club_invitation",
  "club_id": "string",
  "club_name": "Real Madrid",
  "invited_by": "admin_username",
  "timestamp": "2026-03-30T10:30:00Z"
}
```

**Tournament Announcement:**
```json
{
  "type": "tournament_announcement",
  "tournament_id": "string",
  "message": "Tournament started!",
  "announcement_type": "started",
  "timestamp": "2026-03-30T10:30:00Z"
}
```

#### JavaScript Example

```javascript
// Connect
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

// Handle connection
socket.onopen = (e) => {
  console.log('Connected to notifications');
  
  // Send heartbeat every 30 seconds
  setInterval(() => {
    socket.send(JSON.stringify({ type: 'heartbeat' }));
  }, 30000);
};

// Handle messages
socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  
  if (data.type === 'mission_completed') {
    console.log(`Mission completed: ${data.mission_name}`);
    showNotification(`Earned ${data.reward_coins} coins!`);
  } else if (data.type === 'auction_won') {
    console.log(`You won ${data.player_name}!`);
    showNotification(`Auction won for ${data.winning_bid} coins`);
  }
};

// Handle errors
socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Handle disconnect
socket.onclose = (e) => {
  console.log('Disconnected from notifications');
  // Attempt reconnect after 5 seconds
  setTimeout(() => connectNotifications(), 5000);
};
```

---

### ⚽ Live Match Consumer

**URL:** `/ws/matches/{match_id}/`

**Authentication:** Optional (JWT token or public view)

#### Connection Message

**To Client:**
```json
{
  "type": "connection_established",
  "match_id": "m-550e8400-e29b-41d4-a716-446655440000",
  "status": "connected",
  "timestamp": "2026-03-30T10:30:00Z"
}
```

#### Server Messages

**Score Updated:**
```json
{
  "type": "score_updated",
  "match_id": "string",
  "player1_score": 2,
  "player2_score": 1,
  "timestamp": "2026-03-30T10:32:00Z"
}
```

**Match Status Changed:**
```json
{
  "type": "match_status_changed",
  "match_id": "string",
  "status": "live",
  "message": "Match started",
  "timestamp": "2026-03-30T10:30:00Z"
}
```

**Match Completed:**
```json
{
  "type": "match_completed",
  "match_id": "string",
  "winner_id": "player1_id",
  "final_score": "3-1",
  "is_draw": false,
  "timestamp": "2026-03-30T10:45:00Z"
}
```

#### JavaScript Example

```javascript
const matchId = 'm-550e8400-e29b-41d4-a716-446655440000';
const socket = new WebSocket(`ws://localhost:8000/ws/matches/${matchId}/`);

socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  
  if (data.type === 'score_updated') {
    updateScoreboard(data.player1_score, data.player2_score);
  } else if (data.type === 'match_completed') {
    showMatchResult(data.winner_id, data.final_score);
  }
};
```

---

### 💰 Auction Bidding Consumer

**URL:** `/ws/auctions/{auction_id}/`

**Authentication:** Required

#### Server Messages

**Bid Placed:**
```json
{
  "type": "bid_placed",
  "auction_id": "string",
  "bid_amount": 5000,
  "bidder_id": "string",
  "total_bids": 12,
  "current_highest": 5000,
  "previous_bidder": "string",
  "timestamp": "2026-03-30T10:31:00Z"
}
```

**Time Remaining Countdown:**
```json
{
  "type": "time_remaining",
  "auction_id": "string",
  "seconds_remaining": 120,
  "timestamp": "2026-03-30T10:32:00Z"
}
```

**Auction Completed:**
```json
{
  "type": "auction_completed",
  "auction_id": "string",
  "status": "sold",
  "final_bid": 5000,
  "winner_id": "string",
  "player_name": "Ronaldo",
  "timestamp": "2026-03-30T10:45:00Z"
}
```

#### JavaScript Example

```javascript
const auctionId = 'a-550e8400-e29b-41d4-a716-446655440000';
const socket = new WebSocket(`ws://localhost:8000/ws/auctions/${auctionId}/`);

socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  
  if (data.type === 'bid_placed') {
    console.log(`New bid: ${data.bid_amount} coins`);
    updateCurrentBid(data.current_highest);
    updateBidCount(data.total_bids);
  } else if (data.type === 'time_remaining') {
    updateCountdown(data.seconds_remaining);
  }
};
```

---

## 📂 File Upload System

### Match Proof Upload

**Endpoint:** `POST /api/v1/matches/{match_id}/submit-result/`

**File Field:** `proof` (multipart/form-data)

#### Upload Requirements

```
Maximum File Size: 10 MB
Allowed Formats:
  - Images: jpg, jpeg, png, gif
  - Videos: mp4, mov
  - Documents: pdf

Content-Type Validation: Checked server-side
Virus Scanning: TBD
```

#### Upload Example (JavaScript)

```javascript
const formData = new FormData();
formData.append('player1_score', 3);
formData.append('player2_score', 1);
formData.append('proof', fileInput.files[0]); // File object

fetch('/api/v1/matches/match-123/submit-result/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log('Upload successful:', data))
.catch(error => console.error('Upload failed:', error));
```

#### Upload Example (cURL)

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "player1_score=3" \
  -F "player2_score=1" \
  -F "proof=@/path/to/proof.mp4" \
  http://localhost:8000/api/v1/matches/match-123/submit-result/
```

#### Error Handling

```json
{
  "success": false,
  "errors": {
    "proof": [
      "File size must not exceed 10MB",
      "or",
      "Invalid file type. Allowed: jpg, jpeg, png, gif, pdf, mp4, mov"
    ]
  }
}
```

#### Storage

- Files stored in Django MEDIA_ROOT (configurable)
- URL accessible via: `/media/matches/proof_...`
- Full URL in response: `https://api.tournament.com/media/matches/...`

---

## 🧮 Business Logic

### Tournament Flow

```
1. CREATE TOURNAMENT
   ├─ Creator provides: name, format, dates, rules
   ├─ Status: draft
   └─ Creator is NOT auto-added as player

2. REGISTRATION PHASE
   ├─ Status: registration
   ├─ Players join tournament
   ├─ Each join creates TournamentPlayer record
   └─ Max players limit enforced

3. TOURNAMENT ACTIVE
   ├─ Status: active
   ├─ Matches are created/scheduled
   ├─ Players submit results with proof
   └─ Leaderboard auto-updates

4. TOURNAMENT COMPLETED
   ├─ Status: completed
   ├─ Final rankings finalized
   ├─ Prizes distributed
   └─ Cannot accept new players

5. TOURNAMENT CANCELLED
   ├─ Status: cancelled
   ├─ All players refunded/notified
   └─ No matches allowed
```

---

### Match Result Logic

**When player submits result:**

```python
1. Validate:
   - User is one of the match players
   - Match status is "scheduled" or "live"
   - Score is valid (integer >= 0)
   - Proof file valid if provided

2. Auto-determine winner:
   - IF player1_score > player2_score:
       winner = player1, loser = player2
   - ELIF player1_score < player2_score:
       winner = player2, loser = player1
   - ELSE (equal scores):
       is_draw = true, winner = null

3. Update UserStatistics:
   - winner.wins += 1
   - loser.losses += 1
   - (if draw) player1.draws += 1, player2.draws += 1
   - Recalculate win_rate = wins / total_matches

4. Update Leaderboard:
   - winner.points += 3
   - (if draw) player1.points += 1, player2.points += 1
   - Recalculate rankings

5. Create MatchEvent:
   - Log match completion event
   - Record timestamp and proof URL
```

---

### Auction Bidding Logic

**Bid Placement Algorithm:**

```python
1. Validate:
   - Auction status == "live"
   - Current time < auction.end_time
   - bidder_id != current_highest_bidder_id
   - bidder has sufficient coins

2. Calculate minimum next bid:
   MIN_NEXT_BID = MAX(
       current_bid * 1.10,  # 10% increment
       current_bid + 10      # Or 10 coins minimum
   )

3. Validate bid amount:
   IF bid_amount < MIN_NEXT_BID:
       RETURN error: "Bid too low"

4. Place bid:
   - Create AuctionBid record
   - Update Auction:
       current_bid = bid_amount
       highest_bidder_id = bidder_id
       total_bids += 1
   - Deduct coins from bidder (tentative hold)
   - Refund previous highest bidder

5. Broadcast to WebSocket:
   - Send bid_placed event to all watchers
   - Notify outbid users
```

---

### Leaderboard Ranking Algorithm

**Tournament Points System:**

```
Win   = 3 points
Draw  = 1 point
Loss  = 0 points
```

**Ranking Tiebreaker Rules (in order):**

```
1. Higher Points
2. Higher Goal Difference (goals_scored - goals_conceded)
3. More Goals Scored
4. Less Goals Conceded
5. Alphabetical by username
```

**Auto-Recalculation Triggers:**

- Match result submitted
- Match result updated by admin
- Leaderboard update endpoint called
- Tournament status changes

---

### Mission Progress Tracking

**Types of conditions:**

```json
{
  "type": "wins",
  "value": 5
}

{
  "type": "matches_played",
  "value": 10
}

{
  "type": "goals_scored",
  "value": 20
}

{
  "type": "tournaments_participated",
  "value": 2
}

{
  "type": "bidding_attempts",
  "value": 50
}
```

**Auto-Completion Logic:**

```python
# After match completion or action
if user_mission.progress >= user_mission.condition_value:
    user_mission.completed = True
    user_mission.completed_at = datetime.now()
    user_mission.save()
    
    # Send notification
    notify_user(user_id, 'mission_completed', {
        mission_name: mission.title,
        reward: mission.reward
    })
```

---

## 🔒 Security Features

### Password Security

```
Requirements:
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 lowercase letter (a-z)
- At least 1 digit (0-9)

Hashing: Bcrypt (via Django's make_password)
Never: Store plain text passwords
```

### JWT Token Security

```
Algorithm: HS256 (HMAC SHA-256)
Secret Key: Loaded from environment (NEVER hardcoded)
Expiry: 
  - Access: 15 minutes
  - Refresh: 7 days

Storage (Frontend):
- LocalStorage: OK for access_token
- HttpOnly Cookie: BEST for refresh_token
```

### Input Validation

```
All endpoints validate:
- Required fields present
- Field types correct
- String length limits enforced
- Email format valid
- UUID format valid
- Enum values valid
- File sizes within limits
- File types whitelisted

Serializer-level validation prevents:
- Duplicate usernames/emails/tournaments
- Invalid tournament dates
- Negative numbers where invalid
- SQL injection (MongoEngine ORM)
```

### Authorization & Permissions

```
Public Endpoints (no auth):
- Register, Login, Token Refresh
- Get tournaments, leaderboard, missions, clubs
- Browse auctions, reports stats

Authenticated Endpoints (JWT required):
- Update profile, logout
- Submit match results
- Place bids, join clubs
- Start missions, claim rewards
- Create tournaments

Admin-Only Endpoints:
- Create admin accounts
- Approve/reject reports
- Update match results (override)
- Reload ML models
- View all reports

Role-Based:
- Tournament Creator only: manage tournament
- Match Player only: submit results
- Club Owner only: update/delete club
- Tournament Player only: join tournament
```

### Anti-Cheat Measures

```
Report System:
- Only match participants can report
- Proof upload required (screenshots/video)
- Admin review workflow
- Actions: match_voided, player_banned

Admin Actions:
- Void match → Reset scores and stats
- Ban player → Prevent tournament participation
- Review notes → Audit trail
```

### Rate Limiting

```
API Endpoints:
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour
- AI prediction: 500 requests/hour

WebSocket:
- Heartbeat required every 60 seconds
- Disconnected if unresponsive > 120 seconds
```

### CORS Configuration

```
Allowed Origins (configurable):
- http://localhost:3000
- http://127.0.0.1:3000
- https://tournament.com (production)

Allowed Methods: GET, POST, PUT, DELETE, OPTIONS
Allowed Headers: Authorization, Content-Type
Credentials: Allowed
```

---

## 🤖 AI/ML System

### Win Probability Prediction

#### How It Works

**Input:**
```
player1_id: string
player2_id: string
```

**Feature Extraction (11 features per player = 22 total):**

```
For each player:
1. total_matches - Career matches played
2. match_wins - Career wins
3. match_losses - Career losses
4. match_draws - Career draws
5. win_rate - Calculated from matches (0-1)
6. goals_scored - Total goals scored
7. goals_conceded - Total goals allowed
8. goal_difference - Scored - Conceded
9. clean_sheets - Matches with 0 goals conceded
10. points - Total tournament points
11. ranking - Current ranking in system
```

**Feature Transformation:**

```python
# Create feature difference vector (relative strength)
feature_diff = [
    player1_feature[i] - player2_feature[i]
    for i in range(11)
]

# Scale using StandardScaler
feature_diff_scaled = scaler.transform([feature_diff])
```

**Model:**
```
Algorithm: RandomForest Classifier (100 trees, max_depth=10)
Training Data: 250+ historical match results
Metrics: 
  - Test Accuracy: ~87%
  - Precision: 0.87
  - Recall: 0.86
  - F1-Score: 0.865
  - AUC: 0.92
```

**Prediction Output:**

```json
{
  "player1_win_probability": 0.65,
  "player2_win_probability": 0.35,
  "confidence": 0.82
}
```

**Confidence Calculation:**

```python
avg_matches = (player1.total_matches + player2.total_matches) / 2
confidence = MIN(avg_matches / 50, 1.0)
# Higher matches = higher confidence (0-1 scale normalized to 50 matches)
```

#### Caching

```
TTL: 1 hour
Keyed by: (player1_id, player2_id)
Invalidation: When user stats update
Benefit: Reduce model inference time
```

#### Training Script

**Usage:**

```bash
# From backend directory
python scripts/train_model.py

# Output:
# ✓ Loads completed matches from MongoDB
# ✓ Extracts features from player statistics
# ✓ Splits data (80/20 train/test)
# ✓ Scales features with StandardScaler
# ✓ Trains RandomForest classifier
# ✓ Evaluates on test set
# ✓ Saves model + metrics to database
# ✓ Registers as active model

# Model saved to: ml_models/win_prob_model_v1_*.pkl
```

---

## 🚀 How to Run Backend Locally

### Prerequisites

```
Python: 3.9+
Docker: Latest (for MongoDB & Redis)
Git: Latest
```

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Football_Tournament.git
cd Football_Tournament/backend
```

#### 2. Create Python Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Setup Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use any text editor
```

**Required Variables:**

```ini
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# MongoDB
MONGO_DB_NAME=football_tournament
MONGO_HOST=mongodb://localhost:27017

# Redis
REDIS_URL=redis://127.0.0.1:6379/1
CHANNELS_REDIS_URL=redis://127.0.0.1:6379/0

# JWT
JWT_ACCESS_LIFETIME=15
JWT_REFRESH_LIFETIME=7

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### 5. Start MongoDB & Redis (Docker)

```bash
# Start all services
docker-compose up -d

# Verify services
docker-compose ps

# Check MongoDB connection
telnet localhost 27017

# Check Redis connection
redis-cli ping  # Should return "PONG"
```

**Without Docker:** Install and run locally:

```bash
# macOS
brew install mongodb-community redis
brew services start mongodb-community
brew services start redis

# Windows (use WSL or Native installers)
# See: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
```

#### 6. Run Django Migrations (if using PostgreSQL, not needed for MongoDB)

```bash
# Not required for MongoDB/Mongoengine, but run for Django internals
python manage.py makemigrations
python manage.py migrate
```

#### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: (secure password)
```

#### 8. Run Development Server

```bash
# Using Daphne (supports WebSockets)
daphne -b 0.0.0.0 -p 8000 core.asgi:application

# Or using Django's runserver (no WebSocket support)
python manage.py runserver 0.0.0.0:8000
```

**Server Running:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 9. Access Backend

```
API Base URL: http://localhost:8000/api/v1/
Admin: http://localhost:8000/admin/
API Docs: http://localhost:8000/api/docs/
```

#### 10. Test WebSockets (Optional)

```bash
# Install wscat globally
npm install -g wscat

# Connect to notifications
wscat -c ws://localhost:8000/ws/notifications/

# Type messages:
{"type": "heartbeat"}
```

---

## 🔗 Integration Guide for Frontend

### Step-by-Step Integration

#### Step 1: Setup API Client

**Create `api/client.js`:**

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
  constructor() {
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  // Add Authorization header
  getHeaders(contentType = 'application/json') {
    const headers = {
      'Content-Type': contentType,
    };
    
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }
    
    return headers;
  }

  // Fetch wrapper with auto token refresh
  async request(url, options = {}) {
    let response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers: this.getHeaders(options.headers?.['Content-Type']),
    });

    // If 401, try refresh token
    if (response.status === 401 && this.refreshToken) {
      await this.refreshAccessToken();
      response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers: {
          ...this.getHeaders(),
          ...options.headers,
        },
      });
    }

    return response.json();
  }

  // Refresh access token
  async refreshAccessToken() {
    const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: this.refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      this.accessToken = data.access;
      localStorage.setItem('access_token', data.access);
    } else {
      this.logout();
    }
  }

  // Store tokens
  setTokens(access, refresh) {
    this.accessToken = access;
    this.refreshToken = refresh;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  // Clear tokens
  logout() {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

export const apiClient = new APIClient();
```

---

#### Step 2: Implement Authentication

**Create `auth/AuthContext.js`:**

```javascript
import React, { createContext, useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      if (apiClient.accessToken) {
        try {
          const response = await apiClient.request('/auth/profile/');
          if (response.success) {
            setUser(response.data);
          }
        } catch (error) {
          console.error('Auth check failed:', error);
          apiClient.logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const register = async (username, email, password, firstName, lastName) => {
    const response = await apiClient.request('/auth/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        email,
        password,
        password_confirm: password,
        first_name: firstName,
        last_name: lastName,
      }),
    });

    if (response.success) {
      apiClient.setTokens(response.data.access, response.data.refresh);
      setUser(response.data.user);
      return true;
    }
    throw response.errors;
  };

  const login = async (username, password) => {
    const response = await apiClient.request('/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (response.success) {
      apiClient.setTokens(response.data.access, response.data.refresh);
      setUser(response.data.user);
      return true;
    }
    throw response.errors;
  };

  const logout = async () => {
    await apiClient.request('/auth/logout/', {
      method: 'POST',
      body: JSON.stringify({ refresh: apiClient.refreshToken }),
    });
    apiClient.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

---

#### Step 3: Create Tournament

```javascript
// components/TournamentForm.js
import { apiClient } from '../api/client';

const createTournament = async (formData) => {
  const response = await apiClient.request('/tournaments/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: formData.name,
      description: formData.description,
      start_date: formData.startDate.toISOString(),
      end_date: formData.endDate.toISOString(),
      format: formData.format, // 'Knockout' or 'League'
      max_players: formData.maxPlayers,
      prize_pool: formData.prizePool,
      is_public: true,
    }),
  });

  if (response.success) {
    console.log('Tournament created:', response.data);
    return response.data;
  } else {
    console.error('Failed to create tournament:', response.errors);
    throw response.errors;
  }
};
```

---

#### Step 4: Join Tournament

```javascript
const joinTournament = async (tournamentId) => {
  const response = await apiClient.request(
    `/tournaments/${tournamentId}/join/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    }
  );

  if (response.success) {
    console.log('Joined tournament successfully');
    return response.data;
  } else {
    throw response.errors;
  }
};
```

---

#### Step 5: Submit Match Result with File Upload

```javascript
const submitMatchResult = async (matchId, player1Score, player2Score, proofFile) => {
  const formData = new FormData();
  formData.append('player1_score', player1Score);
  formData.append('player2_score', player2Score);
  if (proofFile) {
    formData.append('proof', proofFile);
  }

  const response = await fetch(
    `${API_BASE_URL}/matches/${matchId}/submit-result/`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiClient.accessToken}`,
      },
      body: formData,
    }
  );

  const data = await response.json();
  if (data.success) {
    console.log('Match result submitted:', data.data);
    return data.data;
  } else {
    throw data.errors;
  }
};
```

---

#### Step 6: Connect WebSocket for Real-Time Updates

```javascript
// hooks/useNotifications.js
import { useEffect, useState } from 'react';

export const useNotifications = (userId) => {
  const [notifications, setNotifications] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket(
      `${process.env.REACT_APP_WS_URL || 'ws://localhost:8000'}/ws/notifications/`
    );

    ws.onopen = () => {
      console.log('Connected to notifications');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'mission_completed') {
        setNotifications(prev => [...prev, {
          id: Date.now(),
          title: 'Mission Completed!',
          message: `You completed: ${data.mission_name}`,
          type: 'success',
          reward: data.reward_coins,
        }]);
      } else if (data.type === 'auction_won') {
        setNotifications(prev => [...prev, {
          id: Date.now(),
          title: 'Auction Won!',
          message: `You won ${data.player_name} for ${data.winning_bid} coins`,
          type: 'success',
        }]);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('Disconnected from notifications');
      // Attempt reconnect after 5 seconds
      setTimeout(() => {
        // Reconnect logic
      }, 5000);
    };

    setSocket(ws);

    return () => {
      if (ws) ws.close();
    };
  }, [userId]);

  return { notifications, socket };
};
```

---

#### Step 7: Get Predictions

```javascript
const getWinPrediction = async (player1Id, player2Id) => {
  const response = await apiClient.request('/ml/predict/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      player1_id: player1Id,
      player2_id: player2Id,
      use_cache: true,
    }),
  });

  if (response.success) {
    return {
      player1Probability: response.data.player1_win_probability,
      player2Probability: response.data.player2_win_probability,
      confidence: response.data.confidence,
    };
  }
  throw response.error;
};
```

---

### Common Mistakes to Avoid

❌ **DON'T:**
```javascript
// ❌ Storing access token in sessionStorage (lost on page refresh)
sessionStorage.setItem('token', accessToken);

// ❌ Forgetting Authorization header
fetch('/api/v1/profile/', { method: 'GET' }); // Will return 401

// ❌ Not handling 401 errors
if (response.status === 401) {
  // Token expired, need to refresh!
}

// ❌ Ignoring WebSocket disconnections
// App stops receiving real-time updates

// ❌ Sending file without FormData
const body = { proof: file }; // Wrong!

// ❌ Hardcoding API URLs
const url = 'http://localhost:8000/api/v1/...'; // Use env variables!

// ❌ Blocking on large file uploads
// Freeze UI while uploading
```

✅ **DO:**
```javascript
// ✅ Use localStorage with secure flag
localStorage.setItem('access_token', accessToken);

// ✅ Always include Authorization header
headers: { 'Authorization': `Bearer ${token}` }

// ✅ Implement token refresh logic
if (response.status === 401) {
  await refreshToken();
  // Retry request
}

// ✅ Implement WebSocket reconnection
socket.onclose = () => {
  setTimeout(() => reconnect(), 5000);
};

// ✅ Use FormData for files
const formData = new FormData();
formData.append('proof', file);

// ✅ Use environment variables
const API_URL = process.env.REACT_APP_API_URL;

// ✅ Show progress indicator during uploads
<ProgressBar percent={uploadProgress} />
```

---

## 📦 Sample API Flow

### Complete User Journey: Register → Tournament → Match → Result

#### 1. User Registration

```javascript
// Frontend
const registerResponse = await api.post('/auth/register/', {
  username: 'player_name',
  email: 'player@example.com',
  password: 'Secure@Pass123',
  password_confirm: 'Secure@Pass123',
  first_name: 'John',
  last_name: 'Doe'
});

// Response
{
  "message": "User registered successfully",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "player_name",
    "email": "player@example.com",
    "coins": 0
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

// Frontend stores tokens
localStorage.setItem('access_token', response.access);
localStorage.setItem('refresh_token', response.refresh);
```

---

#### 2. Browse Tournaments

```javascript
// Frontend
const tournamentsResponse = await api.get('/tournaments/?status=registration&format=League');

// Response
{
  "count": 5,
  "results": [
    {
      "tournament_id": "t-123456",
      "name": "Champions League 2026",
      "format": "League",
      "status": "registration",
      "current_players": 8,
      "max_players": 16,
      "start_date": "2026-04-01T10:00:00Z",
      "created_at": "2026-03-30T10:00:00Z"
    }
  ]
}
```

---

#### 3. Join Tournament

```javascript
// Frontend
const joinResponse = await api.post('/tournaments/t-123456/join/', {});

// Response
{
  "message": "Successfully joined tournament",
  "tournament_player": {
    "tournament_player_id": "tp-789",
    "tournament_id": "t-123456",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "player_name",
    "status": "active",
    "joined_at": "2026-03-30T14:30:00Z"
  }
}

// Backend updates:
// - Increments tournament.current_players
// - Creates TournamentPlayer record
```

---

#### 4. Get Tournament Matches

```javascript
// Frontend
const matchesResponse = await api.get('/matches/tournament/t-123456/');

// Response
{
  "results": [
    {
      "match_id": "m-123456",
      "tournament_id": "t-123456",
      "player1_username": "player_name",
      "player2_username": "opponent_name",
      "match_date": "2026-04-01T15:00:00Z",
      "status": "scheduled",
      "score": null,
      "created_at": "2026-03-30T12:00:00Z"
    }
  ]
}
```

---

#### 5. Get Win Prediction

```javascript
// Frontend
const predictionResponse = await api.post('/ml/predict/', {
  player1_id: "550e8400-e29b-41d4-a716-446655440000",
  player2_id: "550e8400-e29b-41d4-a716-446655440001"
});

// Response
{
  "player1_id": "550e8400-e29b-41d4-a716-446655440000",
  "player2_id": "550e8400-e29b-41d4-a716-446655440001",
  "player1_win_probability": 0.65,
  "player2_win_probability": 0.35,
  "confidence": 0.82,
  "predicted_at": "2026-03-30T15:00:00Z"
}

// Frontend displays:
// "You have 65% chance to win this match"
```

---

#### 6. Watch Live Match

```javascript
// Frontend - Connect WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/matches/m-123456/');

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'score_updated') {
    console.log(`Score: ${data.player1_score} - ${data.player2_score}`);
    // Update scoreboard UI
  } else if (data.type === 'match_completed') {
    console.log(`Match over! Winner: ${data.winner_id}`);
    // Show final result
  }
};
```

---

#### 7. Submit Match Result

```javascript
// Frontend
const formData = new FormData();
formData.append('player1_score', 3);
formData.append('player2_score', 1);
formData.append('proof', proofFile); // File from input

const resultResponse = await fetch('/api/v1/matches/m-123456/submit-result/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
  body: formData
});

const data = await resultResponse.json();

// Response
{
  "message": "Match result submitted successfully",
  "data": {
    "match_id": "m-123456",
    "winner_id": "550e8400-e29b-41d4-a716-446655440000",
    "loser_id": "550e8400-e29b-41d4-a716-446655440001",
    "is_draw": false,
    "status": "completed"
  }
}

// Backend updates:
// - Sets winner/loser
// - Updates UserStatistics (wins/losses)
// - Recalculates Leaderboard
// - Sends WebSocket event to all watchers
```

---

#### 8. Check Updated Leaderboard

```javascript
// Frontend
const leaderboardResponse = await api.get('/leaderboard/tournament/t-123456/');

// Response
{
  "tournament_id": "t-123456",
  "leaderboard": [
    {
      "rank": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "player_name",
      "points": 3,
      "wins": 1,
      "losses": 0,
      "draws": 0,
      "goal_difference": 2,
      "win_rate": 100.0
    },
    {
      "rank": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440001",
      "username": "opponent_name",
      "points": 0,
      "wins": 0,
      "losses": 1,
      "draws": 0,
      "goal_difference": -2,
      "win_rate": 0.0
    }
  ]
}

// Frontend displays:
// - Player is now ranked #1
// - 3 points from 1 win
```

---

## 🧪 Testing APIs

### Using Postman

#### 1. Set Base URL Variable

```
Variable Name: base_url
Value: http://localhost:8000/api/v1
```

#### 2. Create Register Request

```
Method: POST
URL: {{base_url}}/auth/register/
Headers:
  Content-Type: application/json

Body (JSON):
{
  "username": "testplayer",
  "email": "test@example.com",
  "password": "Test@Password123",
  "password_confirm": "Test@Password123",
  "first_name": "Test",
  "last_name": "Player"
}
```

#### 3. Store Token in Variable

```
After register response received:
- Click "Tests" tab
- Add script:

var jsonData = pm.response.json();
pm.environment.set("access_token", jsonData.access);
pm.environment.set("refresh_token", jsonData.refresh);
```

#### 4. Use Token in Authenticated Requests

```
Method: GET
URL: {{base_url}}/auth/profile/
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
```

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testplayer",
    "email": "test@example.com",
    "password": "Test@Password123",
    "password_confirm": "Test@Password123"
  }'

# Get Access Token from response, then use it
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Get Profile
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"

# Create Tournament
curl -X POST http://localhost:8000/api/v1/tournaments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Tournament",
    "format": "League",
    "max_players": 16,
    "start_date": "2026-04-01T10:00:00Z",
    "end_date": "2026-05-31T23:59:59Z"
  }'
```

### Using Node.js/JavaScript

```javascript
// test-api.js
const apiUrl = 'http://localhost:8000/api/v1';

// Register
async function register() {
  const res = await fetch(`${apiUrl}/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'testplayer',
      email: 'test@example.com',
      password: 'Test@Password123',
      password_confirm: 'Test@Password123'
    })
  });
  return res.json();
}

// Get Profile  
async function getProfile(token) {
  const res = await fetch(`${apiUrl}/auth/profile/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return res.json();
}

// Run tests
(async () => {
  const registerRes = await register();
  console.log('Registered:', registerRes.user);
  
  const profileRes = await getProfile(registerRes.access);
  console.log('Profile:', profileRes.data);
})();
```

**Run:** `node test-api.js`

---

## 📌 Notes & Future Improvements

### Current Limitations

1. **No Email Verification**
   - Users can register with any email
   - Future: Add email confirmation via OTP

2. **No Real Match Scheduling**
   - Matches manually created
   - Future: Auto-schedule based on tournament format

3. **No Real Payments**
   - Coins are in-game currency only
   - Future: Integrate Stripe/PayPal

4. **Limited ML Model**
   - Only RandomForest with 250 training samples
   - Future: Add more models (XGBoost, Deep Learning)

5. **No Notification Persistence**
   - Real-time only via WebSocket
   - Future: Store notifications in database

6. **No Push Notifications**
   - No mobile/desktop notifications
   - Future: Integrate Firebase Cloud Messaging

### Suggested Improvements

#### Priority 1 (High Impact)

- [ ] **Email Verification**
  - Add verification tokens
  - Send confirmation emails
  - Prevent unverified email spam

- [ ] **Search Across Entities**
  - Search tournaments by name
  - Search clubs, players, missions
  - Add full-text search with filters

- [ ] **Player Statistics API**
  - Detailed career stats
  - Head-to-head comparisons
  - Historical performance trends

- [ ] **Notification Persistence**
  - Store notifications in DB
  - Mark as read/unread
  - Notification center in frontend

#### Priority 2 (Medium Impact)

- [ ] **Admin Dashboard**
  - User management
  - Report moderation
  - Model retraining  UI
  - System analytics

- [ ] **Badge System**
  - Achievement badges
  - Award conditions
  - Display on profile

- [ ] **Payment Integration**
  - Stripe checkout
  - Coin packages
  - Transaction history

- [ ] **Export Data**
  - Export leaderboard CSV
  - Export match history
  - Tournament reports

#### Priority 3 (Nice to Have)

- [ ] **Social Features**
  - Friend lists
  - Player following
  - Direct messaging
  - Player profiles

- [ ] **Advanced Search**
  - Elasticsearch integration
  - Autocomplete
  - Faceted search

- [ ] **Analytics Dashboard**
  - Player charts
  - Tournament analytics
  - Prediction accuracy tracking

- [ ] **Multilingual Support**
  - i18n integration
  - Support multiple languages
  - Regional tournaments

---

### Performance Optimization Ideas

```python
# 1. Add Caching Layer
CACHE_TIMEOUT = 300  # 5 minutes
@cache_page(CACHE_TIMEOUT)
def get_leaderboard(tournament_id):
    pass

# 2. Pagination on Large Queries
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

# 3. Select Related / Prefetch Related
matches = Match.objects.select_related('winner').prefetch_related('events')

# 4. Database Indexing (already done)
# 5. CDN for File Storage
# 6. Background Tasks with Celery
```

---

### Security Enhancements

```python
# 1. Rate Limiting (Already implemented)
# 2. SQL Injection Protection (MongoDB is immune)
# 3. CORS Whitelisting (Already implemented)
# 4. HTTPS/SSL in Production
# 5. API Keys for External Services
# 6. Audit Logging
# 7. Two-Factor Authentication
# 8. Password Reset via Email
```

---

## Final Checklist for Frontend Developers

- [ ] Clone backend repository
- [ ] Create Python virtual environment  
- [ ] Install dependencies from requirements.txt
- [ ] Setup .env file with MongoDB/Redis URLs
- [ ] Start MongoDB and Redis (Docker or local)
- [ ] Run Django server with Daphne
- [ ] Test auth endpoints (register, login)
- [ ] Test tournament endpoints
- [ ] Test match submission with file upload
- [ ] Connect WebSocket for real-time updates
- [ ] Get predictions from ML API
- [ ] Verify all error responses formats
- [ ] Setup API client with token refresh logic
- [ ] Implement proper error handling in UI
- [ ] Test with production-like environment

---

## Support & Contact

**Documentation Issues?**
- Check this file first
- Review API endpoint examples

**Backend Bugs?**
- Create issue on GitHub
- Include error logs

**Feature Requests?**
- Discuss in team
- Add to future improvements list

---

**End of Documentation**

*This guide should provide frontend developers with complete clarity on integrating with the Football Tournament backend without additional questions.*
