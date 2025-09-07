from scipy.io import wavfile

from .synth import Block


def write(data: Block, filename):
    """Write a numpy array as a WAV file."""
    wavfile.write(filename, data.sample_rate, data.samples)
