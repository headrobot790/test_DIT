import logging
import os

from fastapi import APIRouter, File, UploadFile, HTTPException
from starlette.responses import FileResponse

from api.exceptions import FileNotExistException, InvalidUUIDLinkException
from api.schemas.images import ImageUploadResponse, ImageURL
from config import settings

from services.image_service import handle_upload
from services.url_service import is_valid_uuid

router = APIRouter(prefix="/images", tags=["images"])
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    task_id = await handle_upload(file)
    return ImageUploadResponse(task_id=task_id)


@router.get("/resized/{url}")
async def get_image(url: str):
    if not is_valid_uuid(url):
        raise InvalidUUIDLinkException
    folder_path = settings.RESIZED_FOLDER_NAME
    file_path = os.path.join(folder_path, url)
    if not os.path.exists(file_path):
        raise FileNotExistException

    return FileResponse(file_path)



