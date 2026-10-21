import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from shodak.api.errors import ShodakApiError
from shodak.api.health import get_health_status, get_provider_status
from shodak.api.routes.research import router as research_router
from shodak.api.routes.run import router as run_router
from shodak.api.routes.write import router as writer_router
from shodak.api.schemas import HealthApiResponse, ProviderStatus
from shodak.config import settings

api_logger = logging.getLogger("shodak.api")

app = FastAPI(
    title="Shodak API",
    description="Research and Writing API powered by Shodak's multi-agent workflow.",
    version="0.1.0",
)


app.include_router(research_router)
app.include_router(writer_router)
app.include_router(run_router)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    start = time.perf_counter()

    api_logger.info(
        "request_started | request_id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    duration = time.perf_counter() - start

    api_logger.info(
        "request_completed | request_id=%s | status=%s | duration=%.3f",
        request_id,
        response.status_code,
        duration,
    )

    response.headers["X-Request-ID"] = request_id

    return response


@app.get("/")
def root() -> dict[str, str]:
    return {"name": settings.app_name, "status": "running"}


@app.get("/health", response_model=HealthApiResponse)
def health() -> HealthApiResponse:
    providers = [ProviderStatus(**provider) for provider in get_provider_status()]
    return HealthApiResponse(
        status=get_health_status(),
        app_name=settings.app_name,
        environment=settings.environment,
        primary_provider=settings.llm_provider,
        fallback_provider=settings.llm_fallback_provider,
        providers=providers,
    )


@app.exception_handler(ShodakApiError)
async def shodak_api_error_handler(request: Request, exc: ShodakApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.error, "message": exc.message}
    )
