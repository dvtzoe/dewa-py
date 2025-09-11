from typing import override

import numpy as np

from ..block import Block
from .base import Modifier


class Bezier(Modifier):
    """
    Generates a bezier curve using cubic bezier interpolation with custom control points.
    
    Uses a cubic bezier curve with 4 control points. Each control point is specified
    as an (x, y) coordinate tuple where x represents the normalized time position
    (0.0 to 1.0) and y represents the value at that time.

    Parameters:
        points: list[tuple[float, float]] => List of 4 (x, y) coordinate tuples 
            representing the control points. x-values should be in range [0.0, 1.0]
            and will be mapped to the block duration.
    
    Example:
        # Create a smooth S-curve
        bezier = Bezier([(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)])
        
        # Create a custom envelope with peak at 2/3 duration
        envelope = Bezier([(0.0, 0.0), (0.3, 0.8), (0.7, 0.8), (1.0, 0.0)])
    """

    def __init__(self, points: list[tuple[float, float]]):
        if len(points) != 4:
            raise ValueError("Bezier modifier requires exactly 4 control points")
        
        self.points = points
        
        # Extract x and y coordinates
        self.x_coords = [point[0] for point in points]
        self.y_coords = [point[1] for point in points]
        
        # Validate x coordinates are in valid range and monotonic
        for i, x in enumerate(self.x_coords):
            if not (0.0 <= x <= 1.0):
                raise ValueError(f"x-coordinate at index {i} must be between 0.0 and 1.0, got {x}")
        
        if self.x_coords != sorted(self.x_coords):
            raise ValueError("x-coordinates must be in non-decreasing order")

    @override
    def _generate(self, block: Block) -> np.ndarray:
        # Create time array that maps to the full block duration
        sample_indices = np.arange(block.duration, dtype=block.dtype)
        
        # Normalize to 0-1 range based on block duration
        if block.duration == 1:
            t_normalized = np.array([0.0], dtype=block.dtype)
        else:
            t_normalized = sample_indices / (block.duration - 1)
        
        # Map the custom x-coordinates to the normalized time range
        # We need to create a parameter t that goes from 0 to 1 across the span 
        # defined by our x-coordinates
        x_min, x_max = self.x_coords[0], self.x_coords[-1]
        
        # Map the normalized time to the range of our x-coordinates
        t_mapped = x_min + t_normalized * (x_max - x_min)
        
        # For cubic Bezier, we need to reparameterize based on our x coordinates
        # We'll interpolate to find the parameter t for each time point
        t_param = np.interp(t_mapped, self.x_coords, [0.0, 1.0/3.0, 2.0/3.0, 1.0])
        
        # Cubic bezier curve formula: B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
        one_minus_t = 1.0 - t_param
        
        curve = (
            one_minus_t**3 * self.y_coords[0] +
            3 * one_minus_t**2 * t_param * self.y_coords[1] +
            3 * one_minus_t * t_param**2 * self.y_coords[2] +
            t_param**3 * self.y_coords[3]
        )
        
        return curve.astype(block.dtype)