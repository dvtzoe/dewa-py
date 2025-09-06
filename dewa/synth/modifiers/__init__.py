from abc import ABC, abstractmethod

import numpy as np

from ..._global import g


# A base class for all modifiers.
class Modifier(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, dur: int) -> np.ndarray:
        if g.verbose:
            print("You cannot use the base Modifier class directly.")
        pass
