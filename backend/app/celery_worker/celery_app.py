from celery import Celery

# Redis is required locally for the message broker
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.celery_worker.tasks"]
)
