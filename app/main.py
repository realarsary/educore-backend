from fastapi import FastAPI

from app.core.database import engine
from app.core.redis import redis_client
from app.core.minio import minio_client
from app.api.v1.api import api_router
from app.core.config import settings
app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        print("✅ DB connected")

    pong = await redis_client.ping()
    print("✅ Redis connected:", pong)
    
    bucket_exists = await minio_client.bucket_exists(settings.MINIO_BUCKET)
    if not bucket_exists:
        await minio_client.make_bucket(settings.MINIO_BUCKET)
        print(f"✅ MinIO: bucket '{settings.MINIO_BUCKET}' created")
    else:
        print(f"✅ MinIO: bucket '{settings.MINIO_BUCKET}' already exists")

        
@app.get("/")
def root():
    return {"message": "EduCore backend worked"}

app.include_router(api_router, prefix="/api/v1")