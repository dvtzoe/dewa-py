from typing import override

import numpy as np
from scipy import signal

from ..block import Block
from .base import Modifier


class Triangle(Modifier):
    def __init__(self, frequency: float | Block):
        self.frequency: float | Block = frequency

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        t = np.linspace(0.0, block.duration_seconds, block.num_samples, endpoint=False)
        if isinstance(self.frequency, Block):
            if self.frequency.num_samples != block.num_samples:
                mod_samples = np.resize(self.frequency.samples, block.num_samples)
            else:
                mod_samples = self.frequency.samples
            phase = 2 * np.pi * np.cumsum(mod_samples) / block.sample_rate
            wave = signal.sawtooth(phase, 0.5)
        else:
            wave = signal.sawtooth(2 * np.pi * self.frequency * t, 0.5)
        return wave
