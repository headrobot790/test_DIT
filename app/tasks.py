import os

from config import settings
from PIL import Image

from celery import Celery

celery = Celery('tasks', broker=settings.BROKER_URL, backend=settings.RESULT_BACKEND)


@celery.task
def process_image(file_path: str, output_path: str):
    print(f"process_image output path: {output_path}")
    # sleep(10)  #  for imitation CPU BOUND
    try:
        with Image.open(file_path) as img:
            if img.mode in ('RGBA', 'LA'):
                print("картинка оказалась с альфа каналом, конвертим в RGB")
                img = img.convert('RGB')
            img = img.resize((settings.RESIZE_X, settings.RESIZE_Y))
            img.save(output_path)

    except Exception as e:
        print(f"неведомая ранее ошибка {e}")
        #  TODO: log error
    return os.path.basename(output_path)
