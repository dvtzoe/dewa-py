from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .modifier.base import Modifier


class Block:
    """
    Represents a block of audio samples.
    """

    def __init__(
        self,
        duration: int = 0,
        dtype: type = np.float32,
    ):
        self.dtype: type = dtype

        self.duration: int = 0 if duration is None else duration
        self.samples: np.ndarray = (
            np.array([], dtype=self.dtype)
            if duration is None
            else np.zeros(self.duration, dtype=self.dtype)
        )

    def __add__(self, other: Modifier | float | int | np.ndarray):
        if isinstance(other, (int, float, np.ndarray)):
            new_block = Block(self.duration, self.dtype)
            new_block.samples = self.samples + other
            return new_block
        return other + self

    def __mul__(self, other: Modifier | float | int | np.ndarray):
        if isinstance(other, (int, float, np.ndarray)):
            new_block = Block(self.duration, self.dtype)
            new_block.samples = self.samples * other
            return new_block
        return other * self

    def __neg__(self) -> Block:
        new_block = Block(self.duration, self.dtype)
        new_block.samples = -self.samples
        return new_block

    def mount(self, other_block: Block, mount_point: int = 0):
        if self.duration < mount_point + other_block.duration:
            required_samples = mount_point + other_block.duration
            if required_samples > self.duration:
                self.samples = np.resize(self.samples, required_samples)
                self.duration = required_samples

        self.samples[mount_point : mount_point + other_block.duration] += (
            other_block.samples
        )

        return self

    def __radd__(self, other: int | float):
        new_block = Block(self.duration, self.dtype)
        new_block.samples = other + self.samples
        return new_block

    def reverse(self) -> Block:
        new_block = Block(self.duration, self.dtype)
        new_block.samples = np.flip(self.samples)
        return new_block

    def repeat(self, times: int) -> Block:
        if not isinstance(times, int) or times <= 0:
            raise ValueError("Times must be a positive integer.")

        new_duration = self.duration * times
        new_block = Block(new_duration, self.dtype)
        new_block.samples = np.tile(self.samples, times)
        return new_block
