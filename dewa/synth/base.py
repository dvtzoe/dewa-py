from __future__ import annotations

import numpy as np

from .modifiers.base import Modifier


class Dewa:
    def __init__(self, dur: int = 0, position: int | None = None) -> None:
        self.dur: int = dur
        self.pos: int | None = position
        self.samples: np.ndarray = np.zeros(dur, dtype=np.float32)

    def __getitem__(self, key: slice) -> np.ndarray:
        return self.samples[key]

    def __setitem__(self, key: slice, value: np.ndarray) -> None:
        self.samples[key] = value

    def __add__(self, other: Dewa | Modifier | np.ndarray) -> Dewa:
        if isinstance(other, Dewa) or isinstance(other, np.ndarray):
            pos1 = self.pos if self.pos is not None else 0
            pos2 = other.pos if isinstance(other, Dewa) and other.pos is not None else 0
            dur1 = self.dur
            dur2 = other.dur if isinstance(other, Dewa) else len(other)

            added_position = min(pos1, pos2)
            added_duration = max(pos1 + dur1, pos2 + dur2) - added_position

            added = Dewa(dur=added_duration, position=added_position)

            added[pos1:dur1] += self.samples
            added[pos2:dur2] += other.samples if isinstance(other, Dewa) else other
        else:  # Modifier
            added = self + other.render(dur=self.dur)

        return added
