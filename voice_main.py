import asyncio
from pathlib import Path

from app.audio.recorder import record_audio
from app.audio.stt import transcribe_audio
from app.audio.tts import text_to_speech, play_audio
from app.graph import graph


INPUT_AUDIO_FILE = Path("input.wav")
OUTPUT_AUDIO_FILE = Path("response.mp3")

CUSTOMER_ID = "user_002"


async def main() -> None:
    print("=" * 60)
    print("Banking Voice Assistant")
    print("=" * 60)
    print()

    input("Press Enter to start recording...")

    record_audio(
        output_path=INPUT_AUDIO_FILE,
        duration=5,
    )

    print()
    print("Transcribing...")

    text = transcribe_audio(INPUT_AUDIO_FILE)

    print()
    print(f"You said: {text}")

    print()
    print("Processing...")

    result = await graph.ainvoke(
        {
            "query": text,
            "customer_id": CUSTOMER_ID,
        }
    )

    answer = result["answer"]

    print()
    print(f"Assistant: {answer}")

    print()
    print(
        f"[debug] route={result.get('route')} "
        f"tool={result.get('selected_tool')}"
    )

    print()
    print("Generating speech...")

    audio_path = text_to_speech(
        text=answer,
        output_path=OUTPUT_AUDIO_FILE,
    )

    print("Playing response...")

    play_audio(audio_path)


if __name__ == "__main__":
    asyncio.run(main())