from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Tremolo(Modifier):
    def __init__(self, frequency: float, depth: float = 1.0):
        if not 0 <= depth <= 1:
            raise ValueError("Depth must be between 0 and 1.")
        self.frequency = frequency
        self.depth = depth

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
        # LFO for amplitude modulation
        lfo = 0.5 * (1 + np.sin(2 * np.pi * self.frequency * t))  # 0 to 1
        # Apply depth
        tremolo_wave = 1 - self.depth + (self.depth * lfo)
        return tremolo_wave
