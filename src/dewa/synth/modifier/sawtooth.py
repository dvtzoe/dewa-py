from typing import override

import numpy as np
from scipy import signal

from ..block import Block
from .base import Modifier


class Sawtooth(Modifier):
    """
    Generates a sawtooth wave modulator.

    Parameters:
        frequency: float [Hz] | Block | Modifier: Frequency of the sawtooth wave in Hz or a Block
            containing frequency modulation data.
        width: float {0.0-1.0} | Block | Modifier: Width of the sawtooth wave (0.0 = rising ramp,
            1.0 = falling ramp) or a Block containing width modulation data or another Modifier.
    """

    def __init__(
        self, frequency: float | Block | Modifier, width: float | Block | Modifier = 1.0
    ):
        self.frequency = frequency
        self.width = width

    @override
    def _generate(self, block: Block) -> np.ndarray:
        if isinstance(self.frequency, Block):
            t = np.resize(self.frequency.samples, block.duration)
        elif isinstance(self.frequency, Modifier):
            t = self.frequency._generate(block)
        else:
            t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
            t *= self.frequency
        if isinstance(self.width, Block):
            self.width = np.resize(self.width.samples, block.duration)
        elif isinstance(self.width, Modifier):
            self.width = self.width._generate(block)
        wave = signal.sawtooth(2 * np.pi * t, self.width)
        return wave
