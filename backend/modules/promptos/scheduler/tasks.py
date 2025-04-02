from scheduler.celery_app import celery_app
from memory.logger import logger

@celery_app.task
def health_check():
    # Tarefa simples de health check do sistema
    logger.info("Executando health check agendado.")
    return "OK"

@celery_app.task
def cleanup_logs():
    # Tarefa para limpar logs antigos (exemplo simples)
    logger.info("Executando limpeza de logs antigos.")
    # Implemente a lógica de limpeza, se necessário.
    return "Logs limpos"