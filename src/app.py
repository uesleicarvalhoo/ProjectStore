import uvicorn
from elasticapm.contrib.starlette import ElasticAPM
from fastapi import FastAPI

from . import api, web
from .apm import apm
from .core.config import settings

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(ElasticAPM, client=apm)


app.mount(path=f"{settings.BASE_PATH}/api", app=api.app, name="api")
app.mount(path=f"{settings.BASE_PATH}/", app=web.app, name="web")


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
