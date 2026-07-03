from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Standardize API error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            "error_code": exc.__class__.__name__,
            "message": str(exc),
            "details": response.data
        }
        response.data = custom_response_data
    else:
        # Unexpected error (e.g., 500)
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        # We don't necessarily want to swallow the standard Django 500 handler,
        # but in a purely API project we might return a custom 500 response.
        # Returning None lets Django's standard 500 handler take over if we want,
        # but since we are writing an API, it's better to return a standardized JSON.
        # But DRF exception_handler already catches API exceptions.
        pass

    return response
