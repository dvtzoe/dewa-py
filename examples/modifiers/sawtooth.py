import os

from dewa import Block, Sawtooth
from dewa.io import write

# Define the sample rate
sample_rate = 44100

# Create a main audio block of 5 seconds duration
main_block = Block(duration=5 * sample_rate)

# Create a Sawtooth effect with a frequency of 440 Hz and width of 0.5
sawtooth = Sawtooth(period=sample_rate / 440, width=0.5)

# Apply the Sawtooth effect to the main audio block
main_block += sawtooth

# Write the modified audio block to an output file
write(
    main_block,
    os.path.join("out", "sawtooth.wav"),
    sample_rate=sample_rate,
)
