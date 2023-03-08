from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .exceptions import NotFound


def custom_exception_handler(exc, context):
    if isinstance(exc, NotFound):
        # Handle 404 errors
        response_data = {"detail": "Sorry, the resource you requested was not found."}
        response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
    else:
        # Call the default exception handler for all other exceptions
        response = exception_handler(exc, context)

    return response
