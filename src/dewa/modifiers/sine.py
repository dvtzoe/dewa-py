from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Sine(Modifier):
    """
    Sine wave generator.

    Parameters:
        period: float [samples] | Block | Modifier: Period of the sine wave or a Block
            containing frequency modulation data or another Modifier.
    """

    def __init__(self, period: float | Block | Modifier, phase: float = 0.0):
        self.period = period
        self.phase = phase

    @override
    def _generate(self, block: Block) -> np.ndarray:
        if isinstance(self.period, Block):
            t = np.resize(self.period.samples, block.duration)
        elif isinstance(self.period, Modifier):
            t = self.period._generate(block)
        else:
            t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
            t /= self.period
        wave = np.sin(2 * np.pi * t + self.phase).astype(block.dtype)
        return wave
