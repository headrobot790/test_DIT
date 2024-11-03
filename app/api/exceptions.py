from fastapi import HTTPException, status

from config import settings


class ImageException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


supported_formats = settings.SUPPORTED_FORMATS

InvalidFiletype = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверный формат изображения. Допустимые форматы: {}".format(", ".join(supported_formats))
)

Unknown_MIME_Info = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Данный файл не является картинкой, либо поврежден"
)

MaxFileSizeExceedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Превышен максимально допустимый размер файла {} Kb".format(settings.MAX_FILE_SIZE)
)

FileNotExistException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Такого файла не сущетсвует"
)

InvalidUUIDLinkException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
detail="Invalid link format"
)


class CeleryException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, task_id: str, detail: str):
        super().__init__(
            status_code=self.status_code,
            detail=f"Ошибка задачи {task_id} : {detail}"
        )
