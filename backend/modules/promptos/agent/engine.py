from .llm import interpret_prompt
from tools.actions import sync_env, push_zip, generate_architecture
from memory.logger import logger
from memory.mongo import log_action
import asyncio

async def process_prompt(prompt: str):
    logger.info(f"Processando prompt: {prompt}")
    try:
        intent = await interpret_prompt(prompt)
    except Exception as e:
        logger.exception("Erro ao interpretar prompt.")
        return {"message": "Erro ao interpretar o comando.", "success": False}

    result = {"message": f"Comando não reconhecido: {prompt}", "success": False}
    if intent == "sync_env":
        result = await sync_env.run()
    elif intent == "push_zip":
        result = await push_zip.run()
    elif intent == "generate_architecture":
        result = await generate_architecture.run()

    # Registra a ação no MongoDB de forma assíncrona
    asyncio.create_task(log_action(prompt, result))
    
    return result