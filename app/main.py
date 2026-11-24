import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppError
from app.logging_config import setup_logging
from app.routes import router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Coding Round Service")
app.include_router(router)


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error, "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        f"{'.'.join(str(p) for p in e['loc'] if p != 'body')}: {e['msg']}"
        for e in exc.errors()
    ]
    logger.warning("Bad request %s %s: %s", request.method, request.url.path, details)
    return JSONResponse(
        status_code=400,
        content={"error": "BAD_REQUEST", "message": "; ".join(details)},
    )


@app.exception_handler(Exception)
async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "Something went wrong"},
    )


@app.get("/health")
def health() -> dict:
    return {"status": "UP"}
