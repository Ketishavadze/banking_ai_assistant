import asyncio
import time
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

    total_start = time.perf_counter()

    # ----------------------------
    # Recording
    # ----------------------------
    recording_start = time.perf_counter()

    record_audio(
        output_path=INPUT_AUDIO_FILE,
        duration=5,
    )

    recording_time = time.perf_counter() - recording_start

    # ----------------------------
    # Speech-to-text
    # ----------------------------
    print()
    print("Transcribing...")

    stt_start = time.perf_counter()

    text = transcribe_audio(INPUT_AUDIO_FILE)

    stt_time = time.perf_counter() - stt_start

    print()
    print(f"You said: {text}")

    # ----------------------------
    # Agent
    # ----------------------------
    print()
    print("Processing...")

    agent_start = time.perf_counter()

    result = await graph.ainvoke(
        {
            "query": text,
            "customer_id": CUSTOMER_ID,
        }
    )

    agent_time = time.perf_counter() - agent_start

    answer = result["answer"]

    print()
    print(f"Assistant: {answer}")

    print()
    print(
        f"[debug] route={result.get('route')} "
        f"tool={result.get('selected_tool')}"
    )

    # ----------------------------
    # Text-to-speech
    # ----------------------------
    print()
    print("Generating speech...")

    tts_start = time.perf_counter()

    audio_path = text_to_speech(
        text=answer,
        output_path=OUTPUT_AUDIO_FILE,
    )

    tts_time = time.perf_counter() - tts_start

    total_time = time.perf_counter() - total_start

    # ----------------------------
    # Metrics
    # ----------------------------
    print()
    print("=" * 60)
    print("LATENCY")
    print("=" * 60)

    print(f"Recording: {recording_time:.2f} s")
    print(f"STT:       {stt_time:.2f} s")
    print(f"Agent:     {agent_time:.2f} s")
    print(f"TTS:       {tts_time:.2f} s")
    print(f"Total:     {total_time:.2f} s")

    print()
    print("Playing response...")
    system_latency = stt_time + agent_time + tts_time
    print(f"System latency: {system_latency:.2f} s")

    play_audio(audio_path)


if __name__ == "__main__":
    asyncio.run(main())