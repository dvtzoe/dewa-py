from __future__ import annotations

from typing import Any

import numpy as np


class Block:
    """
    Represents a block of audio samples.
    """

    def __init__(
        self,
        duration: int | None = None,
        sample_rate: int = 44100,
        dtype: type = np.float32,
    ):
        self.sample_rate: int = sample_rate
        self.dtype: type = dtype
        self.dynamic_duration: bool = duration is None

        self.duration: int = 0 if duration is None else duration
        self.samples: np.ndarray = (
            np.array([], dtype=self.dtype)
            if duration is None
            else np.zeros(self.duration, dtype=self.dtype)
        )

    def __add__(self, other: Any):  # pyright: ignore[reportAny,reportExplicitAny]
        return other.apply(self, "add")  # pyright: ignore[reportAny]

    def __mul__(self, other: Any):  # pyright: ignore[reportAny,reportExplicitAny]
        return other.apply(self, "multiply")  # pyright: ignore[reportAny]

    def __neg__(self) -> Block:
        new_block = Block(self.duration, self.sample_rate, self.dtype)
        new_block.samples = -self.samples
        return new_block

    def mount(self, other_block: Block, mount_point: int = 0):
        if self.dynamic_duration or self.duration < mount_point + other_block.duration:
            required_samples = mount_point + other_block.duration
            if required_samples > self.duration:
                self.samples = np.resize(self.samples, required_samples)
                self.duration = required_samples

        self.samples[mount_point : mount_point + other_block.duration] += (
            other_block.samples
        )

        return self

    def __radd__(self, other: int | float):
        new_block = Block(self.duration, self.sample_rate, self.dtype)
        new_block.samples = other + self.samples
        return new_block

    def reverse(self) -> Block:
        new_block = Block(self.duration, self.sample_rate, self.dtype)
        new_block.samples = np.flip(self.samples)
        return new_block

    def repeat(self, times: int) -> Block:
        if not isinstance(times, int) or times <= 0:
            raise ValueError("Times must be a positive integer.")

        new_duration = self.duration * times
        new_block = Block(new_duration, self.sample_rate, self.dtype)
        new_block.samples = np.tile(self.samples, times)
        return new_block
