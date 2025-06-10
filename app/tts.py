# app/tts.py
import os
from elevenlabs import generate, play, set_api_key
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def speak_text(text, voice="Monika Sogam - Hindi Modulated"):
    try:
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        play(audio)
    except Exception as e:
        print(f"[TTS Error]: {str(e)}")