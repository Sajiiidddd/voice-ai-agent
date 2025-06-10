# Voice AI Agent

A real-time speech-to-text voice agent built with Python using Deepgram's streaming API.

## Features

- Real-time transcription using [Deepgram API](https://deepgram.com/)
- Live microphone input via `sounddevice`
- Async audio streaming using `websockets`
- `.env` support for managing API keys
- Easy to integrate with downstream voice agents or AI logic

How to Run --> python main.py

## Requirements

- Python 3.10+
- `sounddevice`
- `websockets`
- `numpy`
- `python-dotenv`

Install dependencies:

```bash
pip install -r requirements.txt


