# list_voices.py

from elevenlabs import voices, set_api_key
from dotenv import load_dotenv
import os

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

for voice in voices():
    print(f"✅ {voice.name}")
