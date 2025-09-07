from __future__ import annotations

from typing import Any

import numpy as np


class Block:
    """
    Represents a block of audio samples.
    """

    def __init__(
        self,
        duration_seconds: float,
        sample_rate: int = 44100,
        dtype: type = np.float32,
    ):
        self.sample_rate: int = sample_rate
        self.dtype: type = dtype
        self.duration_seconds: float = duration_seconds
        self.num_samples: int = int(self.duration_seconds * self.sample_rate)
        self.samples: np.ndarray = np.zeros(self.num_samples, dtype=self.dtype)

    def __add__(self, other: Any):  # pyright: ignore[reportAny,reportExplicitAny]
        return other.apply(self, "add")  # pyright: ignore[reportAny]

    def __mul__(self, other: Any):  # pyright: ignore[reportAny,reportExplicitAny]
        return other.apply(self, "multiply")  # pyright: ignore[reportAny]

    def __neg__(self) -> Block:
        new_block = Block(self.duration_seconds, self.sample_rate, self.dtype)
        new_block.samples = -self.samples
        return new_block

    def mount(self, other_block: Block, at_time: float = 0.0):
        start_sample = int(at_time * self.sample_rate)
        if start_sample >= self.num_samples:
            return self
        num_samples_to_add = min(
            other_block.num_samples, self.num_samples - start_sample
        )
        if num_samples_to_add > 0:
            end_sample = start_sample + num_samples_to_add
            self.samples[start_sample:end_sample] += other_block.samples[
                :num_samples_to_add
            ]
        return self

    def __radd__(self, other: int | float):
        new_block = Block(self.duration_seconds, self.sample_rate, self.dtype)
        new_block.samples = other + self.samples
        return new_block

    def reverse(self) -> Block:
        new_block = Block(self.duration_seconds, self.sample_rate, self.dtype)
        new_block.samples = np.flip(self.samples)
        return new_block

    def repeat(self, times: int) -> Block:
        if not isinstance(times, int) or times <= 0:
            raise ValueError("Times must be a positive integer.")

        new_duration = self.duration_seconds * times
        new_block = Block(new_duration, self.sample_rate, self.dtype)
        new_block.samples = np.tile(self.samples, times)
        return new_block
