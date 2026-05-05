from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from app.exceptions.application_error import ApplicationError
from app.models.model_error_response import ErrorResponse
from app.models.model_validation_error_item import ValidationErrorItem
from app.models.model_validation_error_response import ValidationErrorResponse


def _format_location(loc: tuple) -> str:
    parts = [str(item) for item in loc if item != "body"]
    return ".".join(parts) if parts else "body"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def application_error_handler(_: Request, exc: ApplicationError) -> JSONResponse:
        print(f"[application-error] {exc.error}: {exc.message}")
        payload = ErrorResponse(
            status_code=exc.status_code,
            error=exc.error,
            message=exc.message,
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        print(f"[validation-error] {exc.errors()}")
        details = [
            ValidationErrorItem(
                field=_format_location(error["loc"]),
                message=error["msg"],
                error_type=error["type"],
            )
            for error in exc.errors()
        ]
        payload = ValidationErrorResponse(
            status_code=422,
            error="validation_error",
            message="Запрос не прошел валидацию.",
            details=details,
        )
        return JSONResponse(status_code=422, content=payload.model_dump())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        print(f"[http-error] {exc.status_code}: {exc.detail}")
        payload = ErrorResponse(
            status_code=exc.status_code,
            error="http_error",
            message=str(exc.detail),
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())
