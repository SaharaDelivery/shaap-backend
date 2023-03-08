from django.shortcuts import render
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound


def custom_exception_handler(exc, context):
    if isinstance(exc, NotFound):
        # Handle 404 errors
        response_data = {"detail": "Sorry, the resource you requested was not found."}
        response = render("404.html", status=404)
    else:
        # Call the default exception handler for all other exceptions
        response = exception_handler(exc, context)

    return response
