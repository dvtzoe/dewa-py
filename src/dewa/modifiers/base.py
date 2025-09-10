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
    """

    @abstractmethod
    def _generate(self, block: Block) -> np.ndarray:
        """
        Abstract method for concrete modifiers to implement.
        Should return a numpy array of the same length as the block.
        """
        raise NotImplementedError
