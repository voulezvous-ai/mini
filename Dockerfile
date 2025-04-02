# Use imagem leve com Python
FROM python:3.10-slim

# Instalar dependências básicas
RUN apt-get update && apt-get install -y build-essential

# Criar diretório de trabalho
WORKDIR /app

# Copiar tudo
COPY . .

# Entrar na pasta backend
WORKDIR /app/backend

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Rodar o app FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]