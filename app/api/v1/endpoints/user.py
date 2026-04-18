from io import BytesIO
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.core.minio import minio_client
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.services.file_service import FileService
from app.repository.user_repo import UserRepository

router = APIRouter()

user_repo = UserRepository()
service = UserService(user_repo)
file_service = FileService(minio_client)

@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.update_me(db, user, data)


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    ext = file.filename.split(".")[-1]
    object_name = f"avatars/{user.id}.{ext}"

    contents = await file.read()

    await file_service.upload_file(
        file_name=object_name,
        data=BytesIO(contents),  
        length=len(contents), 
        content_type=file.content_type,
    )

    avatar_url = await file_service.get_download_url(object_name)

    return await service.update_me(db, user, UserUpdate(avatar_url=avatar_url))