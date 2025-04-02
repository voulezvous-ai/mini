import openai
import os
from memory.logger import logger

openai.api_key = os.getenv("OPENAI_API_KEY")

async def interpret_prompt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Qual a intenção deste comando?: '{prompt}'"}],
            max_tokens=20,
            timeout=10
        )
        intent = response.choices[0].message.content.strip().lower()
        logger.info(f"Intenção interpretada: {intent}")
        return intent
    except Exception as e:
        logger.exception("Erro na chamada para a API do OpenAI. Tentando fallback...")
        # Fallback multiprovider: aqui você pode integrar outro serviço, como Claude ou similar.
        # Por enquanto, retornaremos um valor padrão para indicar erro.
        return "erro"