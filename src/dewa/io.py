import os
import shutil
from pathlib import Path

import ffmpeg
import numpy as np

from .block import Block


def from_file(file_path: str | Path, sample_rate: int = 44100) -> Block:
    """Loads an audio file into a Block.

    Args:
        file_path: Path to the audio file.
        sample_rate: The sample rate to load the audio at.

    Returns:
        A Block containing the audio data.
    """
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg and ensure it is in your PATH."
        )

    try:
        # Use ffmpeg to read the audio file and convert it to pcm_f32le format
        out, _ = (
            ffmpeg.input(str(file_path))
            .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=str(sample_rate))
            .run(capture_stdout=True, capture_stderr=True)
        )
        audio_data = np.frombuffer(out, np.float32).copy()

    except ffmpeg.Error as e:
        print("ffmpeg stderr:", e.stderr.decode())
        raise

    block = Block(duration=len(audio_data))
    block.samples = audio_data

    return block


def write(data: Block, filename: str, sample_rate: int = 44100):
    """Write a Block to an audio file."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg and ensure it is in your PATH."
        )

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    if os.path.exists(filename):
        print(f"Warning: {filename} already exists and will be overwritten.")
        os.remove(filename)

    try:
        (
            ffmpeg.input(
                "-",
                format="f32le",
                acodec="pcm_f32le",
                ac=1,
                ar=str(sample_rate),
            )
            .output(filename)
            .run(
                input=data.samples.astype(np.float32).tobytes(),
                capture_stdout=True,
                capture_stderr=True,
            )
        )
    except ffmpeg.Error as e:
        print("ffmpeg stderr:", e.stderr.decode())
        raise
