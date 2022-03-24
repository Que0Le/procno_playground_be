from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.mount("/static", StaticFiles(directory="./data/static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=[
            "https://127.0.0.1",
            "https://localhost",
            "https://127.0.0.1:3000",
            "https://localhost:3000",
            "https://localhost:3000/",
            "https://192.168.1.15:3000",
            "https://192.168.1.15:3000/",
            # "http://192.168.1.15:8888"
        ],
        allow_credentials=True,
        allow_methods=["DELETE", "GET", "POST", "PUT"],
        allow_headers=[
            "*",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
            "Access-Control-Allow-Credentials",
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
