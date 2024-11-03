from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DOCS_URL: str = "/docs"
    UPLOAD_FOLDER_NAME: str = "uploads/"
    RESIZED_FOLDER_NAME: str = "resized/"
    BROKER_URL: str = "redis://redis:6379/0"
    RESULT_BACKEND: str = "redis://redis:6379/0"
    SUPPORTED_FORMATS: List[str] = ["jpg", "jpeg", "png"]
    MAX_FILE_SIZE: int = 4096  # set size value in Kb
    RESIZE_X: int = 300
    RESIZE_Y: int = 300

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()