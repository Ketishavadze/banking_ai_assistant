from pathlib import Path

import pygame
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()


def text_to_speech(
    text: str,
    output_path: str | Path = "response.mp3",
) -> Path:
    """
    Convert text into speech and save it as an MP3 file.
    """

    output_path = Path(output_path)

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(output_path)

    return output_path


def play_audio(audio_path: str | Path) -> None:
    """
    Play an audio file through the default speaker.
    """

    pygame.mixer.init()
    pygame.mixer.music.load(str(audio_path))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()