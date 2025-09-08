from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Echo(Modifier):
    """
    Adds an echo effect to the audio block.

    Parameters:
        delay: int [samples] => The delay in samples before the echo starts.
        decay: float | Block | Modifier => The decay factor for the echo amplitude.
    """

    def __init__(self, delay: int, decay: float | Block | Modifier = 0.5):
        self.delay = delay
        self.decay = decay

    @override
    def _generate(self, block: Block) -> np.ndarray:
        echo_wave = np.zeros_like(block.samples)

        if isinstance(self.decay, Block):
            decay = np.resize(self.decay.samples, block.duration)
        elif isinstance(self.decay, Modifier):
            decay = self.decay._generate(block)
        else:
            decay = self.decay

        echo_wave[: self.delay] = block.samples[: self.delay]

        for i in range(self.delay, block.duration):
            echo_wave[i] = block.samples[i] + echo_wave[i - self.delay] * decay

        return echo_wave
