import uvicorn
from elasticapm.contrib.starlette import ElasticAPM
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import api, web
from .core.config import settings
from .core.helpers.database import init_database
from .core.helpers.logger import logger
from .monitoring import monitoring_client

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.mount(path=f"{settings.BASE_PATH}/api", app=api.app, name="api")
app.mount(path=f"{settings.BASE_PATH}/", app=web.app, name="web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "https://localhost",
    ],
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

if monitoring_client:
    app.add_middleware(ElasticAPM, client=monitoring_client)


@app.on_event("startup")
async def app_init_database():
    logger.info("Starting database, creating initial data..")
    init_database()
    logger.info("Database started, initial data created.")


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
