import asyncio
import time
from app.stt import DeepgramSTT
from app.llm import generate_response
from app.tts import speak_text
from app.metrics import MetricsLogger

class VoiceAgent:
    def __init__(self):
        self.stt = DeepgramSTT()
        self.logger = MetricsLogger()

    async def run(self):
        print("\U0001f9e0 Voice Agent is active. Speak into the mic...\n")

        async def on_transcript(transcript):
            print(f"\U0001f5e3️ You: {transcript}")
            t_eou = self.logger.start_timer()

            # LLM Response
            t_llm_start = time.perf_counter()
            ai_reply = generate_response(transcript)
            t_ttft = time.perf_counter()

            print(f"\U0001f916 AI: {ai_reply}")

            # TTS Playback
            t_ttfb = time.perf_counter()
            speak_text(ai_reply)

            # Log metrics
            self.logger.log_turn(transcript, ai_reply, t_eou, t_ttft, t_ttfb)

        # Run the transcription with callback
        await self.stt.transcribe(on_transcript)

def run_agent():
    agent = VoiceAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user. Saving metrics...")
        agent.logger.save_to_excel()

if __name__ == "__main__":
    run_agent()


