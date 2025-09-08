from typing import override

import numpy as np
from scipy import signal

from ..block import Block
from .base import Modifier


class Sawtooth(Modifier):
    """
    Generates a sawtooth wave modulator.

    Parameters:
        frequency (float | Block): Frequency of the sawtooth wave in Hz or a Block
                                   containing frequency modulation data.
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
            wave = signal.sawtooth(phase)
        else:
            wave = signal.sawtooth(2 * np.pi * self.frequency * t)
        return wave
