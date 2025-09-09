import os

from dewa import Block, LinearRamp
from dewa.io import write

# Define the sample rate
sample_rate = 44100

# Create a main audio block of 5 seconds duration
main_block = Block(duration=5 * sample_rate)

# Create a linear ramp effect with start at 0.0 and end at 1.0
linear_ramp = LinearRamp(start=0.0, end=1.0)

# Apply the LinearRamp effect to the main audio block
main_block += linear_ramp

# Write the modified audio block to an output file
write(
    main_block,
    os.path.join("out", "linear_ramp.wav"),
    sample_rate=sample_rate,
)
