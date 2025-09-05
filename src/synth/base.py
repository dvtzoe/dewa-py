from __future__ import annotations

import numpy as np


class Dewa:
    def __init__(self, dur: int = 0, position: int | None = None) -> None:
        self.dur: int = dur
        self.pos: int | None = position
        self.samples: np.ndarray = np.zeros(dur, dtype=np.float32)

    def __getitem__(self, key: slice) -> np.ndarray:
        return self.samples[key]

    def __setitem__(self, key: slice, value: np.ndarray) -> None:
        self.samples[key] = value

    def __add__(self, other: Dewa) -> Dewa:
        if self.pos is None or other.pos is None:
            raise ValueError("Both Dewa instances must have a defined position.")
        added_position = min(self.pos, other.pos)
        added_duration = (
            max(self.pos + self.dur, other.pos + other.dur) - added_position
        )

        added = Dewa(dur=added_duration, position=added_position)

        added[self.pos : self.dur] += self.samples
        added[other.pos : other.dur] += other.samples

        return added

