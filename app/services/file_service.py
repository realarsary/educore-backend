from miniopy_async import Minio
from app.core.config import settings
from datetime import timedelta

class FileService:

    def __init__(self, client: Minio):
        self.client = client
        self.bucket = settings.MINIO_BUCKET

    async def upload_file(self, file_name: str, data, length: int, content_type: str) -> str:
        await self.client.put_object(
            bucket_name=self.bucket,
            object_name=file_name,
            data=data,
            length=length,
            content_type=content_type,
        )
        return file_name

    async def get_url(self, file_name: str, expires: int = 3600) -> str:
        url = await self.client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=file_name,
            expires=timedelta(seconds=expires),
        )
        return url

    async def delete_file(self, file_name: str):
        await self.client.remove_object(
            bucket_name=self.bucket,
            object_name=file_name,
        )
    
 

    async def get_upload_url(self, object_name: str, expires: int = 3600) -> str:
        url = await self.client.presigned_put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            expires=timedelta(seconds=expires),
        )
        return url

    async def get_download_url(self, object_name: str, expires: int = 3600) -> str:
        url = await self.client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=object_name,
            expires=timedelta(seconds=expires),
        )
        return url

    async def file_exists(self, object_name: str) -> bool:
        try:
            await self.client.stat_object(self.bucket, object_name)
            return True
        except Exception:
            return False