from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
# import logging
from fastapi import FastAPI


# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# ch = logging.StreamHandler()
# # fh = logging.handlers.RotatingFileHandler("api.log",mode="a",maxBytes = 100*1024, backupCount = 3)
# fh = logging.FileHandler(filename=f"{settings.DATA_PATH}/logs/server.log") #TODO: file too large
# formatter = logging.Formatter(
#     "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
# )

# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# logger.addHandler(ch) #Exporting logs to the screen
# logger.addHandler(fh) #Exporting logs to a file


# logger = logging.getLogger(__name__)
# logger.info("Starting app ...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    terms_of_service="",
    # contact={
    #     "name": "Deadpoolio the Amazing",
    #     "url": "http://x-force.example.com/contact/",
    #     "email": "dp@x-force.example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# app.mount("/static", StaticFiles(directory=f"{settings.DATA_PATH}/static"), name="static")

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
