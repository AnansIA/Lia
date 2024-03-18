from gtts import gTTS
import random
from config import configurations


def crear_audio(text, path='', lang='es'):
    tts = gTTS(text=text, lang=lang)
    if not path:
        configs = configurations()
        path = configs.read_config('files', 'audios')
    num = random.randint(1, 9999)
    name = f"audios_{num}.mp3" 
    tts.save(path + name)
    return name

