from fastapi import FastAPI

from app.core.database import engine
from app.core.redis import redis_client
from app.api.v1.api import api_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        print("✅ DB connected")

    pong = await redis_client.ping()
    print("✅ Redis connected:", pong)


@app.get("/")
def root():
    return {"message": "EduCore backend worked"}

app.include_router(api_router, prefix="/api/v1")