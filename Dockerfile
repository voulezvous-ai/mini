FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY . .

# Aqui entramos no diretório correto
WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt

# Aqui executamos diretamente sem 'backend.'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
