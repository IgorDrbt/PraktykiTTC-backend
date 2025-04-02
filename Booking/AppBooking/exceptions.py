from rest_framework.views import exception_handler
from rest_framework.response import response
from rest_framework import status

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                "error": True,
                "massage": response.data if isinstance(response.data, dict) else str(exc)
            },
            status=response.status_code
        )

    return Response(
        {
            "error": True,
            "messege": "Wystąpił nieoczekiwany błąd serwera."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )