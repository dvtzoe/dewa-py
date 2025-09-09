import os

from dewa import Echo
from dewa.io import read, write

# Define the sample rate
sample_rate = 44100

# Read the main audio block from a sample file
main_block = read(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "samples", "metal_pipe.opus"
    )
)

# Create an Echo effect with a delay of 5000 ms and a decay factor of 0.6
echo = Echo(delay=5000, decay=0.6)

# Apply the Echo effect to the main audio block
main_block += echo

# Write the modified audio block to an output file
write(
    main_block,
    os.path.join("out", "echo.wav"),
    sample_rate=sample_rate,
)
