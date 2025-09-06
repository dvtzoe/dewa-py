from typing import override

import numpy as np

from ..._global import g
from .__init__ import Modifier


class Sine(Modifier):
    def __init__(
        self,
        freq: float = 440.0,
        amp: float = 1.0,
        phase: float = 0.0,
        x: np.ndarray | str = "linear",
    ) -> None:
        super().__init__()
        self.freq: float = freq
        self.amp: float = amp
        self.phase: float = phase
        self.x: np.ndarray | str = x

    @override
    def render(self, dur: int) -> np.ndarray:
        if isinstance(self.x, str):
            if self.x == "linear":
                t = np.linspace(0, dur / g.sample_rate, dur, endpoint=False)
            else:
                raise ValueError(f"Unknown x type: {self.x}")
        else:
            t = self.x
        return self.amp * np.sin(2 * np.pi * self.freq * t + self.phase)
