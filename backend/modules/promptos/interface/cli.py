import sys
from pathlib import Path
import asyncio

# Ajusta o path para importar os módulos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "agent"))
sys.path.append(str(BASE_DIR / "memory"))
sys.path.append(str(BASE_DIR / "tools"))
sys.path.append(str(BASE_DIR / "interface"))

from engine import process_prompt
from memory.logger import logger
from voice import speak

def main():
    print("\n🧠 PromptOS - Modo Interativo CLI\n")
    while True:
        try:
            user_input = input("PromptOS 🧠 > ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Desligando o sistema. Até mais!")
                break
            logger.info(f"Input do usuário: {user_input}")
            result = asyncio.run(process_prompt(user_input))
            message = result.get("message", "")
            print(f"🤖 Resposta: {message}")
            logger.info(f"Resposta: {result}")
            # Se o resultado indicar que deve falar, aciona o módulo de voz.
            if result.get("speak"):
                speak(message)
        except KeyboardInterrupt:
            print("\nInterrompido. Encerrando.")
            break
        except Exception as e:
            print(f"⚠️ Erro: {e}")
            logger.exception("Erro no CLI.")

if __name__ == "__main__":
    main()