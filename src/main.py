import os

from scipy.io import wavfile

from ._global import g


def main():
    if g.verbose:
        print("Verbose mode enabled")

    os.makedirs(os.path.dirname(g.output), exist_ok=True)
    wavfile.write(g.output, g.sample_rate, g.data)
