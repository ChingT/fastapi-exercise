from celery import Celery
from celery.result import AsyncResult

from app.core.config import settings


class Config:
    CELERY_BROKER_URL: str = settings.CELERY_BROKER_URL
    result_backend: str = settings.CELERY_RESULT_BACKEND
    broker_connection_retry_on_startup: bool = True


def create_celery():
    celery_app = Celery()
    celery_app.config_from_object(Config())
    return celery_app


def get_task_info(task_id):
    """Return task info for the given task_id."""
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
