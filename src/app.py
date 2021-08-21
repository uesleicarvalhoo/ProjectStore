import uvicorn
from elasticapm.contrib.starlette import ElasticAPM
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from starlette import status
from starlette.requests import Request

from src.api import health_check, v1
from src.apm import apm
from src.core.config import settings
from src.core.exceptions import DatabaseError, NotFoundError

app = FastAPI(
    title="Bia Rommanel",
    version=settings.VERSION,
    description="Serviço de controle de vendas da Romannel para Bia bonitona!",
    docs_url=f"{settings.BASE_PATH}/docs",
    redoc_url=f"{settings.BASE_PATH}/redoc",
    openapi_url=f"{settings.BASE_PATH}/openapi.json",
    default_response_class=UJSONResponse,
)


app.add_middleware(ElasticAPM, client=apm)

app.include_router(v1.router, prefix=f"{settings.BASE_PATH}/v1")
app.include_router(health_check.router, prefix=f"{settings.BASE_PATH}/health")


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


if __name__ == "__main__":
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
