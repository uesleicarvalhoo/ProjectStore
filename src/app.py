from elasticapm.contrib.starlette import ElasticAPM
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse

from .api import auth, health_check, v1
from .core.config import settings
from .core.helpers.database import init_database
from .core.helpers.exceptions import DatabaseError, InvalidCredentialError, NotFoundError
from .core.helpers.logger import logger
from .monitoring import capture_exception, monitoring_client

app = FastAPI(
    title="ProjectStore - API",
    version=settings.VERSION,
    description="API for backend of Projectstore",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=UJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

if monitoring_client:
    app.add_middleware(ElasticAPM, client=monitoring_client)


app.include_router(v1.endpoints, prefix="/v1")
app.include_router(health_check.router, prefix="/health")
app.include_router(auth.router, prefix="/auth")


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_error(request: Request, exc: RequestValidationError):
    capture_exception()
    return UJSONResponse(content={"message": exc.errors()}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    capture_exception()
    return UJSONResponse(content={"message": exc.detail}, status_code=exc.status_code)


@app.exception_handler(DatabaseError)
async def database_error(request: Request, exc: DatabaseError):
    capture_exception()
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(InvalidCredentialError)
async def invalid_credential_error(request: Request, exc: InvalidCredentialError):
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(NotFoundError)
async def not_found_error(request: Request, exc: NotFoundError):
    capture_exception()
    return UJSONResponse(content={"message": exc.detail}, status_code=status.HTTP_204_NO_CONTENT)


@app.exception_handler(Exception)
async def unknown_error(request: Request, exc: Exception):
    capture_exception()
    return UJSONResponse(content={"message": str(exc)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.on_event("startup")
async def app_init_database():
    logger.info("Starting database, creating initial data..")
    init_database()
    logger.info("Database started, initial data created.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        log_level="info",
        access_log=True,
        workers=settings.WORKERS,
        timeout_keep_alive=50,
    )
