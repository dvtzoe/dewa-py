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

# Create a bezier curve envelope for smooth fade-in and fade-out
# Using (x, y) coordinate tuples: (time_position, amplitude)
# This creates an envelope that starts at 0, rises to full volume, then fades out
bezier_envelope = Bezier([(0.0, 0.0), (0.3, 0.8), (0.7, 0.8), (1.0, 0.0)])

# Apply the Bezier envelope to the main audio block
main_block *= bezier_envelope

# Write the modified audio block to an output file
write(
    main_block,
    os.path.join("out", "bezier_envelope.wav"),
    sample_rate=sample_rate,
)