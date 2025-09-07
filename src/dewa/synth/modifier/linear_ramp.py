from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class LinearRamp(Modifier):
    def __init__(self, start: float, end: float):
        self.start: float = start
        self.end: float = end

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        ramp: np.ndarray = np.linspace(  # pyright: ignore[reportUnknownVariableType]
            self.start, self.end, block.num_samples, endpoint=False, dtype=block.dtype
        )
        return ramp
