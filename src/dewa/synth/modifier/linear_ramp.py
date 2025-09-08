from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class LinearRamp(Modifier):
    """
    Generates a linear ramp from start to end over the duration of the block.

    Parameters:
        start: float => The starting value of the ramp.
        end: float => The ending value of the ramp.
    """

    def __init__(self, start: float, end: float):
        self.start: float = start
        self.end: float = end

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        ramp: np.ndarray = np.linspace(  # pyright: ignore[reportUnknownVariableType]
            self.start, self.end, block.duration, endpoint=False, dtype=block.dtype
        )
        return ramp
