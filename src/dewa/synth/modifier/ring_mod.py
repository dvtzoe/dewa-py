from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class RingMod(Modifier):
    """
    Applies ring modulation to the audio block using a sine wave modulator.

    Parameters:
        frequency: float [Hz] => Frequency of the modulating sine wave.
    """

    def __init__(self, frequency: float):
        self.frequency = frequency

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
        modulator = np.sin(2 * np.pi * self.frequency * t)
        return modulator
