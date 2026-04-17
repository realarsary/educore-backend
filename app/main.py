from fastapi import FastAPI
from app.core.database import engine
from app.core.redis import redis_client

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
