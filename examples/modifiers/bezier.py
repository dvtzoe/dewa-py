import os

from dewa import Block
from dewa.modifiers import Bezier, Sine
from dewa.io import write

# Define the sample rate
sample_rate = 44100

# Create a main audio block of 3 seconds duration
main_block = Block(duration=3 * sample_rate)

# Add a sine wave
main_block += Sine(440)

# Demonstrate different Bezier curve types

# 1. Quadratic Bezier (3 points) - simple peak envelope
print("Creating quadratic Bezier envelope...")
quadratic_envelope = Bezier([(0.0, 0.0), (0.5, 1.0), (1.0, 0.0)])

# Apply the quadratic envelope to a copy of the main block
quadratic_block = Block(main_block.samples.copy()) * quadratic_envelope

# Write the quadratic envelope audio
write(
    quadratic_block,
    os.path.join("out", "bezier_quadratic.wav"),
    sample_rate=sample_rate,
)

# 2. Cubic Bezier (4 points) - smooth fade-in and fade-out
print("Creating cubic Bezier envelope...")
cubic_envelope = Bezier([(0.0, 0.0), (0.3, 0.8), (0.7, 0.8), (1.0, 0.0)])

# Apply the cubic envelope to a copy of the main block
cubic_block = Block(main_block.samples.copy()) * cubic_envelope

# Write the cubic envelope audio
write(
    cubic_block,
    os.path.join("out", "bezier_cubic.wav"),
    sample_rate=sample_rate,
)

# 3. Higher-order Bezier (5 points) - complex envelope with multiple peaks
print("Creating quintic Bezier envelope...")
quintic_envelope = Bezier([(0.0, 0.0), (0.2, 0.6), (0.5, 1.0), (0.8, 0.4), (1.0, 0.0)])

# Apply the quintic envelope to a copy of the main block
quintic_block = Block(main_block.samples.copy()) * quintic_envelope

# Write the quintic envelope audio
write(
    quintic_block,
    os.path.join("out", "bezier_quintic.wav"),
    sample_rate=sample_rate,
)

print("Generated three different Bezier curve examples:")
print("- bezier_quadratic.wav (3 control points)")
print("- bezier_cubic.wav (4 control points)")  
print("- bezier_quintic.wav (5 control points)")