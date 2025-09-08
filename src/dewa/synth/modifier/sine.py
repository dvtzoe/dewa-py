from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Sine(Modifier):
    """
    Sine wave generator.
    """

    def __init__(self, frequency: float | Block):
        self.frequency: float | Block = frequency

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
        if isinstance(self.frequency, Block):
            if self.frequency.duration != block.duration:
                mod_samples = np.resize(self.frequency.samples, block.duration)
            else:
                mod_samples = self.frequency.samples
            phase = 2 * np.pi * np.cumsum(mod_samples) / block.sample_rate
            wave = np.sin(phase)
        else:
            wave = np.sin(2 * np.pi * self.frequency * t)
        return wave
