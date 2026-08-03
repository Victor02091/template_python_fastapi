from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI) -> None:
    """Register application middlewares."""
    app.add_middleware(
        CORSMiddleware,
        # Allow all origins for CORS. In production,
        # you may want to restrict this to specific domains.
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
