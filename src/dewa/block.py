from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .modifiers.base import Modifier


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
            self.samples = np.zeros(duration, dtype=self.dtype)

    def __add__(self, other: Modifier | float | int | np.ndarray | Block):
        if isinstance(other, (float, int, np.ndarray)):
            return Block(self.samples + other, dtype=self.dtype)
        elif isinstance(other, Block):
            resized_other = np.resize(other.samples, self.duration)
            return Block(self.samples + resized_other, dtype=self.dtype)
        else:
            return Block(self.samples + other._generate(self), dtype=self.dtype)

    def __mul__(self, other: Modifier | float | int | np.ndarray | Block) -> Block:
        if isinstance(other, (float, int, np.ndarray)):
            return Block(self.samples * other, dtype=self.dtype)
        elif isinstance(other, Block):
            resized_other = np.resize(other.samples, self.duration)
            return Block(self.samples * resized_other, dtype=self.dtype)
        else:
            return Block(self.samples * other._generate(self), dtype=self.dtype)

    def mount(self, other_block: Block, mount_point: int = 0) -> Block:
        if self.duration < mount_point + other_block.duration:
            required_samples = mount_point + other_block.duration
            self.samples = np.resize(self, required_samples)

        self.samples[mount_point : mount_point + other_block.duration] += (
            other_block.samples
        )

        return self

    def concat(self, other_block: Block | np.ndarray) -> Block:
        if isinstance(other_block, Block):
            concatenated_samples = np.concatenate((self.samples, other_block.samples))
        else:
            concatenated_samples = np.concatenate((self.samples, other_block))
        self.samples = concatenated_samples
        return self

    def __array__(self) -> np.ndarray:
        return self.samples

    @property
    def duration(self) -> int:
        return len(self.samples)

    def __repr__(self) -> str:
        return f"Block(duration={self.duration}, dtype={self.dtype}):\n{self.samples}"
