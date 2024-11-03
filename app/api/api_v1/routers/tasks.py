from fastapi import APIRouter, Request

from api.exceptions import CeleryException
from celery.result import AsyncResult


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/status/{task_id}")
async def get_status(task_id: str, request: Request):
    task = AsyncResult(task_id)
    if task.state == "SUCCESS":
        file_id = task.result.split("/")[-1]
        full_url = request.url_for("get_image", url=file_id)._url
        return {
            "status": task.state,
            "url": full_url
        }
    elif task.state == "FAILURE":
        raise CeleryException(task_id=task_id, detail=str(task.info))
    return {"status": task.state}