from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from memory.logger import logger

class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.exception("Erro não tratado.")
            return JSONResponse(
                status_code=500,
                content={"detail": "Ocorreu um erro inesperado", "error": str(e)}
            )