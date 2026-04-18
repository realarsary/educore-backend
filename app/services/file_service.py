from miniopy_async import Minio
from app.core.config import settings


class FileService:

    def __init__(self, client: Minio):
        self.client = client
        self.bucket = settings.MINIO_BUCKET

    async def ensure_bucket(self):
        exists = await self.client.bucket_exists(self.bucket)
        if not exists:
            await self.client.make_bucket(self.bucket)

    async def upload_file(self, file_name: str, data, length: int, content_type: str) -> str:
        await self.ensure_bucket()
        await self.client.put_object(
            bucket_name=self.bucket,
            object_name=file_name,
            data=data,
            length=length,
            content_type=content_type,
        )
        return file_name

    async def get_url(self, file_name: str, expires: int = 3600) -> str:
        from datetime import timedelta
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