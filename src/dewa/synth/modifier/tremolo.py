from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Tremolo(Modifier):
    """
    Tremolo effect generator.
    Parameters:
        frequency: float [Hz] | Block | Modifier: Frequency of the tremolo effect in Hz or a Block
            containing frequency modulation data or another Modifier
        depth: float {0.0-1.0} | Block | Modifier: Depth of the tremolo effect (0.0 = no effect,
            1.0 = full effect) or a Block containing depth modulation data or another Modifier
    """

    def __init__(
        self, frequency: float | Block | Modifier, depth: float | Block | Modifier = 1.0
    ):
        self.frequency = frequency
        self.depth = depth

    @override
    def _generate(self, block: Block) -> np.ndarray:
        if isinstance(self.frequency, Block):
            t = np.resize(self.frequency.samples, block.duration)
        elif isinstance(self.frequency, Modifier):
            t = self.frequency._generate(block)
        else:
            t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
            t *= self.frequency
        if isinstance(self.depth, Block):
            self.depth = np.resize(self.depth.samples, block.duration)
        elif isinstance(self.depth, Modifier):
            self.depth = self.depth._generate(block)

        lfo = 0.5 * (1 + np.sin(2 * np.pi * t))
        tremolo_wave = 1 - self.depth + (self.depth * lfo)
        return tremolo_wave
