from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Echo(Modifier):
    """
    Adds an echo effect to the audio block.

    Parameters:
        delay: int [samples] => The delay in samples before the echo starts.
        decay: float {0 < decay < 1} => The decay factor for the echo amplitude.
    """

    def __init__(self, delay: int, decay: float = 0.5):
        if not 0 <= decay <= 1:
            raise ValueError("Decay must be between 0 and 1.")
        self.delay = delay
        self.decay = decay

    @override
    def _generate_wave(self, block: Block) -> np.ndarray:
        echo_wave = np.zeros_like(block.samples)

        for i in range(self.delay, block.duration):
            echo_wave[i] = block.samples[i - self.delay] * self.decay

        return echo_wave
