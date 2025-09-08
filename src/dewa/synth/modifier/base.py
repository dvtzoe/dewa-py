from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..block import Block


class Modifier(ABC):
    """
    Base class for all modifiers.
    Modifiers can apply transformations to audio blocks by generating a wave
    and either adding or multiplying it with the block's samples.

    Methods:
        _generate_wave(block: Block) -> np.ndarray:
            Abstract method to generate the modulating wave.
        apply(block: Block, operation: str) -> Block:
            Applies the generated wave to the block's samples using the specified operation.
    """

    @abstractmethod
    def _generate_wave(self, block: Block) -> np.ndarray:
        """
        Abstract method for concrete modifiers to implement.
        Should return a numpy array of the same length as the block.
        """
        raise NotImplementedError

    def apply(self, block: Block, operation: str) -> Block:
        wave = self._generate_wave(block)

        if wave.shape != block.samples.shape:
            raise ValueError("Generated wave shape does not match block samples shape.")

        if operation == "add":
            block.samples += wave
        elif operation == "multiply":
            block.samples *= wave

        return block
