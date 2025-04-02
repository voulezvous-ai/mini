import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "promptos",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["scheduler.tasks"]
)

celery_app.conf.beat_schedule = {
    "health-check": {
        "task": "scheduler.tasks.health_check",
        "schedule": 300.0,  # Executa a cada 5 minutos
    },
    "cleanup-logs": {
        "task": "scheduler.tasks.cleanup_logs",
        "schedule": 3600.0,  # Executa a cada 1 hora
    },
}

if __name__ == "__main__":
    celery_app.start()