import os
from fastapi import FastAPI, Header, HTTPException, Depends
from reasoning.error_handler import GlobalExceptionMiddleware
from memory.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

# Inicializa o Sentry para monitoramento de erros
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", "YOUR_SENTRY_DSN"),
    traces_sample_rate=1.0
)

app = FastAPI(title="PromptOS", docs_url="/docs", redoc_url="/redoc")

# Configuração de CORS – ajuste conforme necessário para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware global para tratamento de exceções
app.add_middleware(GlobalExceptionMiddleware)
# Middleware do Sentry para captura de erros
app.add_middleware(SentryAsgiMiddleware)

def verify_api_key(x_api_key: str = Header(...)):
    expected_api_key = os.getenv("API_KEY")
    if not expected_api_key or x_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

@app.on_event("startup")
async def startup_event():
    logger.info("PromptOS está iniciando...")

@app.get("/status", tags=["Status"])
async def status(api_key: str = Depends(verify_api_key)):
    logger.info("Status verificado.")
    return {"status": "PromptOS está online."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent.main:app", host="0.0.0.0", port=8000, reload=False)