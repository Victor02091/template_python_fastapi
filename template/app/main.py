import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import setup_middlewares
from app.services.health import get_health_status

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="{{ project_name }}",
    description="{{ description }}",
    version="0.1.0",
)
setup_middlewares(app)
app.include_router(api_router, prefix="/api")

logger.info("Application startup configured")


@app.get("/health", response_class=PlainTextResponse)
async def health() -> str:
    return get_health_status()
