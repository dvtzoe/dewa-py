import shutil

import ffmpeg
import numpy as np

from .synth import Block


def write(data: Block, filename: str, sample_rate: int = 44100):
    """Write a Block to an audio file."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg and ensure it is in your PATH."
        )

    try:
        (
            ffmpeg.input(
                "-",
                format="f32le",
                acodec="pcm_f32le",
                ac=1,
                ar=str(sample_rate),
            )
            .output(filename, format="wav")
            .run(input=data.samples.astype(np.float32).tobytes(), capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print("ffmpeg stderr:", e.stderr.decode())
        raise
