from rest_framework.views import exception_handler
from rest_framework.response import Response
from resident_management.core.exceptions import BaseException
from resident_management.core.utils.response import error


def custom_exception_handler(exc, context):
    if isinstance(exc, BaseException):
        return Response(
            error(message=exc.message, code=exc.code, errors=exc.errors),
            status=exc.status_code,
        )
    
    response = exception_handler(exc, context)
    if response:
        detail = response.data.get("detail", "An error occurred")
        return Response(
            error(message=str(detail), code=response.status_code),
            status=response.status_code,
        )
    
    return Response(error(message="Internal server error", code=500), status=500)