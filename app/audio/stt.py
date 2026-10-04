from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()


def transcribe_audio(audio_path: str | Path) -> str:
    """
    Transcribe a recorded audio file into text using OpenAI STT.
    """

    audio_path = Path(audio_path)

    with audio_path.open("rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )

    return transcription.text