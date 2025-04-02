from loguru import logger
import sys
import os

# Remove handlers padrão para evitar duplicidade
logger.remove()

# Logging no console
logger.add(sys.stdout, format="<green>{time}</green> <level>{message}</level>", level="INFO")

# Logging em arquivo com rotação e compressão
log_file = os.path.join(os.path.dirname(__file__), "agentos.log")
logger.add(log_file, rotation="1 MB", retention="10 days", compression="zip")