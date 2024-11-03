from pydantic import BaseModel, Field


class ImageUploadResponse(BaseModel):
    task_id: str


class ImageURL(BaseModel):
    url: str
