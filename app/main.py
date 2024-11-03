import logging
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.api_v1.routers.images import router as image_router
from api.api_v1.routers.tasks import router as task_router
from config import settings


def create_img_folders_on_startup():
    os.makedirs(settings.UPLOAD_FOLDER_NAME, exist_ok=True)
    os.makedirs(settings.RESIZED_FOLDER_NAME, exist_ok=True)


def create_app() -> FastAPI:

    create_img_folders_on_startup()
    app = FastAPI(
        title='Simple Image Resizer',
        docs_url=settings.DOCS_URL,
        description='A simple resizer for uploaded images',
        debug=True,
    )
    app.mount("/resized_pictures", StaticFiles(directory=settings.RESIZED_FOLDER_NAME))

    app.include_router(image_router)
    app.include_router(task_router)

    return app



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')




