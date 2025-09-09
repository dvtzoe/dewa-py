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
        samples: np.ndarray | None = None,
        duration: int = 0,
        dtype: type = np.float32,
    ):
        self.dtype: type = dtype

        if samples is not None:
            self.samples = samples.astype(self.dtype)
        else:
            self.samples = np.zeros(self.duration, dtype=self.dtype)

    def __add__(self, other: Modifier | float | int | np.ndarray):
        if isinstance(other, (int, float, np.ndarray)):
            new_block = Block(dtype=self.dtype)
            new_block.samples = self.samples + other
            return new_block
        return other + self

    def __mul__(self, other: Modifier | float | int | np.ndarray):
        if isinstance(other, Modifier):
            return other * self
        return Block(self.samples * other, dtype=self.dtype)

    def __neg__(self) -> Block:
        return Block(-self.samples, dtype=self.dtype)

    def mount(self, other_block: Block, mount_point: int = 0):
        if self.duration < mount_point + other_block.duration:
            required_samples = mount_point + other_block.duration
            if required_samples > self.duration:
                self.samples = np.resize(self.samples, required_samples)

        self.samples[mount_point : mount_point + other_block.duration] += (
            other_block.samples
        )

        return self

    def reverse(self) -> Block:
        return Block(np.flip(self.samples), dtype=self.dtype)

    def repeat(self, times: int) -> Block:
        return Block(np.tile(self.samples, times), dtype=self.dtype)

    def __len__(self) -> int:
        return len(self.samples)

    @property
    def duration(self) -> int:
        return len(self.samples)
