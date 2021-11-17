from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import RedirectResponse

from src.core.config import settings
from src.core.helpers.exceptions import DataValidationError, InvalidCredentialError, NotAuthorizedError
from src.core.models import Context
from src.monitoring import capture_exception
from src.utils.dependencies import refresh_access_token, validate_access_token, web_context_manager

from . import views
from .utils import send_message, templates

__version__ = "0.0.0"

app = FastAPI(
    title="Store - Web",
    version=__version__,
    description="Template app for e-commerce",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=HTMLResponse,
)

app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
app.include_router(views.endpoints)


@app.middleware("http")
async def refresh_session(request: Request, call_next: RequestResponseEndpoint):
    cookie_token: str = request.cookies.get(settings.ACCESS_TOKEN_NAME, None)
    session_id: str = request.cookies.get(settings.SESSION_KEY_NAME, None)

    response = await call_next(request)

    if (
        cookie_token
        and validate_access_token(cookie_token)
        and not any(path in request.url.path for path in ["/login", "/logout", "/static", "favicon"])
    ):
        await refresh_access_token(response=response, token=cookie_token)

    if not session_id:
        response.set_cookie(settings.SESSION_KEY_NAME, str(uuid4()))

    return response


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def http_404_not_found(
    request: Request,
    exc: Exception,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse(
        "not_found.html",
        context={"request": request, "error": exc, "context": context},
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found_error(
    request: Request,
    exc: Exception,
    context: Context = Depends(web_context_manager),
):
    return templates.TemplateResponse(
        "not_found.html",
        context={"request": request, "error": exc, "context": context},
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(NotAuthorizedError)
async def not_authorized(request: Request, exc: NotAuthorizedError):
    send_message(
        request,
        "Acesso não autorizado",
        exc.detail,
    )
    return RedirectResponse(request.url_for("web:login"), status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(InvalidCredentialError)
async def invalid_credentials(request: Request, exc: InvalidCredentialError):
    send_message(
        request,
        "Acesso não autorizado",
        exc.detail,
    )

    return RedirectResponse(request.url_for("web:login"), status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(RequestValidationError)
async def schema_validation_error(
    request: Request,
    exc: RequestValidationError,
    context: Context = Depends(web_context_manager),
):
    capture_exception()

    return templates.TemplateResponse(
        "error.html",
        context={
            "request": request,
            "error": exc,
            "context": context,
            "error_description": "422 - Dados de entrada invalidos",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(DataValidationError)
async def validation_error(
    request: Request,
    exc: DataValidationError,
    context: Context = Depends(web_context_manager),
):
    send_message(request, header="Dados de entrada invalidos!", text=exc.detail)
    return templates.TemplateResponse(
        "error.html",
        context={
            "request": request,
            "error": exc,
            "context": context,
            "error_description": f"422 - {exc.detail}",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(Exception)
async def error(
    request: Request,
    exc: Exception,
    context: Context = Depends(web_context_manager),
):

    capture_exception()
    return templates.TemplateResponse(
        "error.html",
        context={
            "request": request,
            "error": exc,
            "context": context,
            "error_description": f"400 - Erro interno, detalhes: {exc}",
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )
