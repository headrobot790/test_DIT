import os
import uuid
from fastapi import UploadFile
from io import BytesIO
from PIL import Image

from api.exceptions import InvalidFiletype, MaxFileSizeExceedException, Unknown_MIME_Info, supported_formats
from config import settings
from tasks import process_image


async def handle_upload(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise InvalidFiletype

    income_file_path = await save_file(file)

    if not await valid_image(income_file_path):
        os.remove(income_file_path)
        raise Unknown_MIME_Info

    income_full_filename = os.path.basename(income_file_path)
    file_name = os.path.splitext(income_full_filename)[0] + "_" + str(settings.RESIZE_X) + "x" + str(settings.RESIZE_Y)
    file_extension = os.path.splitext(income_full_filename)[1]
    output_file_path = os.path.join(settings.RESIZED_FOLDER_NAME, file_name + file_extension)
    task = process_image.apply_async(args=[income_file_path, output_file_path])
    return task.id


async def save_file(file: UploadFile) -> str:
    extension = file.filename.split(".")[-1]
    file_id = str(uuid.uuid4())
    income_file_path = os.path.join(settings.UPLOAD_FOLDER_NAME, file_id + "." + extension)

    file_data = await file.read()
    with open(income_file_path, "wb") as buffer:
        buffer.write(file_data)

    return income_file_path


async def valid_image(file_path: os.path) -> bool:
    try:
        with open(file_path, "rb") as image_file:
            image_data = image_file.read()

            if len(image_data) == 0:
                return False

            if len(image_data) > settings.MAX_FILE_SIZE * 1024:
                raise MaxFileSizeExceedException

            image_io = BytesIO(image_data)
            img = Image.open(image_io)
            img.verify()
            if img.format.lower() not in supported_formats:
                return False
            return True
    except IOError:
        print("IOError")
        return False
    except Exception as e:
        print("Неизведанная ранее ошибка: {}".format(e))
        #  TODO: log unknown errors
        return False
