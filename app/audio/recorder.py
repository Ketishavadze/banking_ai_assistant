from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write


SAMPLE_RATE = 16000
CHANNELS = 1


def record_audio(
    output_path: str | Path,
    duration: int = 5,
) -> Path:
    """
    Record audio from the default microphone and save it as a WAV file.

    Args:
        output_path:
            Location where the WAV file should be saved.

        duration:
            Number of seconds to record.

    Returns:
        Path to the saved audio file.
    """

    output_path = Path(output_path)

    print(f"Recording for {duration} seconds...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
    )

    sd.wait()

    write(
        output_path,
        SAMPLE_RATE,
        audio,
    )

    print(f"Recording saved to: {output_path}")

    return output_path