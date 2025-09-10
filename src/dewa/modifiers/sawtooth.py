from typing import override

import numpy as np
from scipy import signal

from ..block import Block
from .base import Modifier


class Sawtooth(Modifier):
    """
    Generates a sawtooth wave modulator.

    Parameters:
        period: float [samples] | Block | Modifier: Period of the sawtooth wave or a Block
            containing period modulation data or another Modifier.
        width: float {0.0-1.0} | Block | Modifier: Width of the sawtooth wave (0.0 = rising ramp,
            1.0 = falling ramp) or a Block containing width modulation data or another Modifier.
    """

    def __init__(
        self,
        period: float | Block | Modifier,
        phase: float = 0.0,
        width: float | Block | Modifier = 1.0,
    ):
        self.period = period
        self.phase = phase
        self.width = width

    @override
    def _generate(self, block: Block) -> np.ndarray:
        if isinstance(self.period, Block):
            t = np.resize(self.period.samples, block.duration)
        elif isinstance(self.period, Modifier):
            t = self.period._generate(block)
        else:
            t = np.linspace(0.0, block.duration, block.duration, endpoint=False)
            t /= self.period
        if isinstance(self.width, Block):
            width = np.resize(self.width.samples, block.duration)
        elif isinstance(self.width, Modifier):
            width = self.width._generate(block)
        else:
            width = self.width
        wave = signal.sawtooth(2 * np.pi * t + self.phase, width)
        return wave
