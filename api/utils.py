from rest_framework.response import Response


def json_response(
    status: int = 200, data: dict = None, message: str = None
) -> Response:
    if data is None:
        data = {}
    if message is None:
        message = ""

    return Response(
        status=status,
        data={"status": "ok", "detail": {"message": message, "data": data}},
    )


def json_response_error(
    status: int = 500, data: dict = None, message: str = None
) -> Response:
    match status:
        case 400:
            error = "400 Bad Request"
        case 404:
            error = "404 Not Found"
        case 500:
            error = "500 Internal Server Error"
    if data is None:
        data = {}
    if message is None:
        message = ""

    return Response(
        status=status,
        data={
            "status": "error",
            "detail": {"error": error, "message": message, "data": data},
        },
    )
