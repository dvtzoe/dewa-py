from typing import override

import numpy as np
from scipy import signal

from ..block import Block
from .base import Modifier


class Triangle(Modifier):
    """
    Triangle wave generator.

    Parameters:
        frequency: float [Hz] | Block | Modifier: Frequency of the triangle wave in Hz or a Block
            containing frequency modulation data or another Modifier
    """

    def __init__(self, frequency: float | Block | Modifier):
        self.frequency = frequency

    @override
    def _generate(self, block: Block) -> np.ndarray:
        if isinstance(self.frequency, Block):
            t = np.resize(self.frequency.samples, block.duration)
        elif isinstance(self.frequency, Modifier):
            t = self.frequency._generate(block)
        else:
            t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
            t *= self.frequency
        wave = signal.sawtooth(2 * np.pi * t, 0.5)
        return wave
