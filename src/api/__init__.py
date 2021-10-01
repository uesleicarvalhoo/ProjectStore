from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import UJSONResponse

from src.apm import apm
from src.core.config import settings
from src.core.helpers.exceptions import DatabaseError, NotFoundError

from . import health_check, v1

app = FastAPI(
    title="Store - API",
    version=settings.VERSION,
    description="Template app for e-commerce",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=UJSONResponse,
)


app.include_router(v1.endpoints, prefix="/v1")
app.include_router(health_check.router, prefix="/health")


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_error(request: Request, exc: RequestValidationError):
    apm.capture_exception()
    return UJSONResponse(content={"message": exc.errors()}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    apm.capture_exception()
    return UJSONResponse(content={"message": exc.detail}, status_code=exc.status_code)


@app.exception_handler(DatabaseError)
async def database_error(request: Request, exc: DatabaseError):
    apm.capture_exception()
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NotFoundError)
async def not_found_error(request: Request, exc: NotFoundError):
    apm.capture_exception()
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_204_NO_CONTENT)


@app.exception_handler(Exception)
async def unknown_error(request: Request, exc: Exception):
    apm.capture_exception()
    return UJSONResponse(content={"message": str(exc)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
