from typing import override
from math import comb

import numpy as np

from ..block import Block
from .base import Modifier


class Bezier(Modifier):
    """
    Generates a bezier curve with dynamic number of control points.
    
    Supports bezier curves of any order:
    - 2 points: Linear interpolation
    - 3 points: Quadratic bezier curve  
    - 4 points: Cubic bezier curve
    - n points: n-1 order bezier curve
    
    Each control point is specified as an (x, y) coordinate tuple where x represents 
    the normalized time position (0.0 to 1.0) and y represents the value at that time.

    Parameters:
        points: list[tuple[float, float]] => List of (x, y) coordinate tuples 
            representing the control points. x-values should be in range [0.0, 1.0]
            and will be mapped to the block duration. Minimum 2 points required.
    
    Examples:
        # Linear interpolation (2 points)
        linear = Bezier([(0.0, 0.0), (1.0, 1.0)])
        
        # Quadratic bezier curve (3 points)
        quadratic = Bezier([(0.0, 0.0), (0.5, 1.0), (1.0, 0.0)])
        
        # Cubic bezier curve (4 points)
        cubic = Bezier([(0.0, 0.0), (0.3, 0.8), (0.7, 0.8), (1.0, 0.0)])
        
        # Higher order curve (5 points)
        quintic = Bezier([(0.0, 0.0), (0.2, 0.5), (0.5, 1.0), (0.8, 0.5), (1.0, 0.0)])
    """

    def __init__(self, points: list[tuple[float, float]]):
        if len(points) < 2:
            raise ValueError("Bezier modifier requires at least 2 control points")
        
        self.points = points
        self.n = len(points)  # Number of control points
        
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
        x_min, x_max = self.x_coords[0], self.x_coords[-1]
        
        # Map the normalized time to the range of our x-coordinates
        t_mapped = x_min + t_normalized * (x_max - x_min)
        
        # Create evenly spaced parameter values for n control points
        if self.n == 1:
            param_values = [0.0]
        else:
            param_values = [i / (self.n - 1) for i in range(self.n)]
        
        # Interpolate to find the parameter t for each time point
        t_param = np.interp(t_mapped, self.x_coords, param_values)
        
        # General Bezier curve formula: B(t) = Σ(i=0 to n-1) [C(n-1,i) * (1-t)^(n-1-i) * t^i * Pi]
        # where C(n-1,i) is the binomial coefficient
        n_minus_1 = self.n - 1
        curve = np.zeros_like(t_param, dtype=block.dtype)
        
        for i in range(self.n):
            # Binomial coefficient C(n-1, i)
            binomial_coeff = comb(n_minus_1, i)
            
            # Bernstein basis polynomial
            basis = binomial_coeff * ((1.0 - t_param) ** (n_minus_1 - i)) * (t_param ** i)
            
            # Add contribution of this control point
            curve += basis * self.y_coords[i]
        
        return curve.astype(block.dtype)