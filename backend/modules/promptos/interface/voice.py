from gtts import gTTS
import os
import tempfile
import platform
import subprocess

def speak(text):
    try:
        tts = gTTS(text, lang='pt')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_file = fp.name
            tts.save(temp_file)
        # Tenta reproduzir o áudio de acordo com o sistema operacional
        if platform.system() == "Darwin":
            subprocess.call(["afplay", temp_file])
        elif platform.system() == "Linux":
            # Certifique-se de que o mpg123 esteja instalado (sudo apt-get install mpg123)
            subprocess.call(["mpg123", temp_file])
        elif platform.system() == "Windows":
            os.startfile(temp_file)
        else:
            print(f"[Vox]: {text}")
    except Exception as e:
        print(f"[Vox]: Erro ao sintetizar voz: {e}")
        print(f"[Vox]: {text}")