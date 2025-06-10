import asyncio
import websockets
import json
import base64
import sounddevice as sd
import numpy as np
import queue
import os
import logging
from dotenv import load_dotenv

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.stt")

# === Load API Key ===
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# === Constants ===
DEEPGRAM_WS_URL = "wss://api.deepgram.com/v1/listen"
SAMPLE_RATE = 16000
RETRY_LIMIT = 5


class DeepgramSTT:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"SoundDevice status: {status}")
        self.q.put(bytes(indata))

    async def send_audio(self, websocket):
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.callback,
            ):
                logger.info("🎙️ Microphone opened, streaming...")
                while True:
                    data = self.q.get()
                    audio_data = base64.b64encode(data).decode('utf-8')
                    await websocket.send(json.dumps({"audio": audio_data}))
        except Exception as e:
            logger.exception("Error in send_audio")
            raise

    async def transcribe(self, on_transcript):
        uri = f"{DEEPGRAM_WS_URL}?punctuate=true&language=en&encoding=linear16&sample_rate={self.sample_rate}"
        headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}

        attempt = 0
        while attempt < RETRY_LIMIT:
            try:
                async with websockets.connect(uri, additional_headers=headers) as websocket:
                    logger.info("🎧 Connected to Deepgram WebSocket")

                    async def receive():
                        try:
                            async for msg in websocket:
                                response = json.loads(msg)
                                transcript = (
                                    response.get("channel", {})
                                    .get("alternatives", [{}])[0]
                                    .get("transcript", "")
                                )
                                if transcript:
                                    await on_transcript(transcript)
                        except websockets.exceptions.ConnectionClosedError as e:
                            logger.error(f"WebSocket closed: {e}")
                        except Exception as e:
                            logger.exception("Error in receive loop")

                    await asyncio.gather(self.send_audio(websocket), receive())
            except Exception as e:
                attempt += 1
                logger.error(f"[Attempt {attempt}/{RETRY_LIMIT}] Connection error: {e}")
                await asyncio.sleep(5)

        logger.critical("🛑 Max retries reached. Could not connect to Deepgram.")


class VoiceAgent:
    def __init__(self):
        self.stt = DeepgramSTT()

    async def run(self):
        logger.info("🧠 Voice Agent is active. Speak into the mic...")

        async def on_transcript(transcript):
            logger.info(f"🗣️ You: {transcript}")
            # === Add your custom logic here ===
            # For example:
            if "weather" in transcript.lower():
                logger.info("🌦️ You asked for the weather (add API logic)")
            elif "joke" in transcript.lower():
                logger.info("😂 You want a joke (add response logic)")
            elif "stop" in transcript.lower():
                logger.info("🛑 Stopping Voice Agent...")
                raise KeyboardInterrupt()

        await self.stt.transcribe(on_transcript)


def run_agent():
    agent = VoiceAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("\n🛑 Interrupted by user.")
    except Exception as e:
        logger.exception("Unexpected error in agent")


if __name__ == "__main__":
    run_agent()















