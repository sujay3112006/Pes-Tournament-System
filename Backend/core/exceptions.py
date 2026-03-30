"""
Custom exception handlers for the API.
"""

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    response = drf_exception_handler(exc, context)
    
    if response is None:
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return Response(
            {
                'error': 'An unexpected error occurred',
                'detail': str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Customize error response format
    if 'detail' in response.data:
        response.data = {
            'error': True,
            'message': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code,
        }
    
    return response
