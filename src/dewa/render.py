from scipy.io import wavfile

from .synth import Block


def write(data: Block, filename):
    """Write a Block to a WAV file."""
    wavfile.write(filename, data.sample_rate, data.samples)
