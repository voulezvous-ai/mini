FROM python:3.10-slim

# Atualiza o sistema e instala dependências básicas de build
RUN apt-get update && apt-get install -y build-essential

# Define a pasta raiz do projeto
WORKDIR /app

# Copia todos os arquivos para dentro do container
COPY . .

# Entra na pasta backend (onde está o main.py)
WORKDIR /app/backend

# Atualiza o pip e instala as dependências, incluindo o uvicorn completo
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install "uvicorn[standard]"

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
