from celery import Celery

from app.core.config import settings


class Config:
    CELERY_BROKER_URL: str = settings.CELERY_BROKER_URL
    result_backend: str = settings.CELERY_RESULT_BACKEND
    broker_connection_retry_on_startup: bool = True


def create_celery():
    celery_app = Celery()
    celery_app.config_from_object(Config())
    return celery_app
