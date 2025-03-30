from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        return Response(
            {"detail": str(exc), "code": "authentication_failed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
