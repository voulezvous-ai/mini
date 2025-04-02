FROM python:3.10-slim

# Atualiza o sistema e instala dependências básicas de build
RUN apt-get update && apt-get install -y build-essential

# Define a pasta raiz do projeto
WORKDIR /app

# Copia todos os arquivos para dentro do container
COPY . .

# Define o path do python
ENV PYTHONPATH=/app

# Instala as dependências do backend
# (Assume que requirements.txt está em /app/backend ou que copiamos antes)
# Copiando requirements.txt primeiro para otimizar o cache
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.txt \
    && pip install "uvicorn[standard]"

# Expor a porta que a aplicação vai usar (opcional mas boa prática)
# A porta real será definida pelo Railway ou variável PORT
EXPOSE 8000

# Comando para iniciar o servidor FastAPI a partir do diretório /app
# O Railway irá provavelmente substituir a porta 8000 pela variável $PORT
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
