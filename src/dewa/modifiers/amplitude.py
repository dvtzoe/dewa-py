from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Amplitude(Modifier):
    """
    Amplitude modifier.

    Parameters:
        amplitude: float [samples] | Block | Modifier: Amplitude of the wave or a Block
            containing data or another Modifier.
    """

    def __init__(self, amplitude: float | Block | Modifier):
        self.amplitude = amplitude

    @override
    def _generate(self, block: Block) -> np.ndarray:
        if isinstance(self.amplitude, Block):
            t = np.resize(self.amplitude.samples, block.duration)
        elif isinstance(self.amplitude, Modifier):
            t = self.amplitude._generate(block)
        else:
            t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
            t /= self.amplitude
        return t
