from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, data, users, topics, answers, small

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(answers.router, prefix="/answers", tags=["answers"])
api_router.include_router(small.router_roles, prefix="/roles", tags=["roles"])
api_router.include_router(small.router_tags, prefix="/tags", tags=["tags"])
api_router.include_router(small.router_records, prefix="/records", tags=["records"])
api_router.include_router(small.router_commentars, prefix="/commentars", tags=["commentars"])
api_router.include_router(small.router_read_texts, prefix="/read-texts", tags=["read_texts"])
api_router.include_router(data.router, prefix="/data", tags=["data"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
