from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Bezier(Modifier):
    """
    Generates a bezier curve from start to end over the duration of the block.
    
    Uses a cubic bezier curve with 4 control points. The control points are
    automatically distributed along the time axis at t=0, t=1/3, t=2/3, and t=1.

    Parameters:
        p0: float => The y-value of the first control point (at t=0).
        p1: float => The y-value of the second control point (at t=1/3).
        p2: float => The y-value of the third control point (at t=2/3).
        p3: float => The y-value of the fourth control point (at t=1).
    """

    def __init__(self, p0: float, p1: float, p2: float, p3: float):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    @override
    def _generate(self, block: Block) -> np.ndarray:
        # Create normalized time array from 0 to 1
        t = np.linspace(0.0, 1.0, block.duration, endpoint=False, dtype=block.dtype)
        
        # Cubic bezier curve formula: B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
        one_minus_t = 1.0 - t
        
        curve = (
            one_minus_t**3 * self.p0 +
            3 * one_minus_t**2 * t * self.p1 +
            3 * one_minus_t * t**2 * self.p2 +
            t**3 * self.p3
        )
        
        return curve.astype(block.dtype)