"""Custom authentication backends for the application."""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import User
import logging

logger = logging.getLogger(__name__)

# Simple in-memory token store (in production, use Redis or database)
_token_store = {}


def generate_token(user_id):
    """Generate and store a token for a user."""
    import secrets
    token = secrets.token_urlsafe(32)
    _token_store[token] = user_id
    logger.info(f"✅ Token generated for user: {user_id}")
    return token


def validate_token(token):
    """Validate a token and return the user_id."""
    if token in _token_store:
        logger.info(f"✅ Token valid for user_id: {_token_store[token]}")
        return _token_store[token]
    logger.warning(f"❌ Invalid token: {token}")
    return None


class SimpleTokenAuthentication(BaseAuthentication):
    """
    Simple token authentication for development/testing.
    Validates Bearer tokens and returns actual User objects.
    """
    
    keyword = 'Bearer'

    def authenticate(self, request):
        """
        Authenticate the request using a Bearer token from Authorization header.
        """
        # Get Authorization header manually
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            logger.debug(f"⚠️ No Authorization header in request to {request.path}")
            return None

        try:
            auth_parts = auth_header.split()
        except Exception as e:
            logger.warning(f"❌ Failed to parse Authorization header: {str(e)}")
            raise AuthenticationFailed('Invalid Authorization header format.')

        if not auth_parts or auth_parts[0].lower() != self.keyword.lower():
            logger.debug(f"⚠️ Authorization header doesn't start with '{self.keyword}'")
            return None

        if len(auth_parts) == 1:
            msg = '❌ Invalid token header. No credentials provided.'
            logger.warning(msg)
            raise AuthenticationFailed(msg)
        elif len(auth_parts) > 2:
            msg = '❌ Invalid token header. Token string should not contain spaces.'
            logger.warning(msg)
            raise AuthenticationFailed(msg)

        token = auth_parts[1]
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """
        Authenticate the token and return the User object.
        """
        logger.info(f"🔐 Validating token: {token[:10]}...")
        
        # Validate token against store
        user_id = validate_token(token)
        if not user_id:
            logger.error(f"❌ Invalid or expired token")
            raise AuthenticationFailed('Invalid or expired token.')

        try:
            # Get actual user from database
            user = User.objects.get(user_id=user_id)
            if not user.is_active:
                logger.warning(f"❌ User inactive: {user_id}")
                raise AuthenticationFailed('User is inactive.')
            
            logger.info(f"✅ Authentication successful for user: {user.username}")
            return (user, token)
        except User.DoesNotExist:
            logger.error(f"❌ User not found: {user_id}")
            raise AuthenticationFailed('User not found.')
        except Exception as e:
            logger.error(f"❌ Authentication error: {str(e)}")
            raise AuthenticationFailed('Authentication failed.')

    def authenticate_header(self, request):
        return self.keyword


