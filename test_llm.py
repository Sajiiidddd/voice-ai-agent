# test_llm.py
from app.llm import generate_response

if __name__ == "__main__":
    prompt = "Tell me a fun fact about space."
    reply = generate_response(prompt)
    print("🤖 Gemini:", reply)
