import fastapi


class HTTPBadRequest(fastapi.HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=detail or "Bad request.",
        )


class HTTPNotAuthenticated(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )


class HTTPForbidden(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )
