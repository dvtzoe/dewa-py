import os

from dewa import Block, Sine
from dewa.io import write

sample_rate = 48000

main_block = Block(duration=5 * sample_rate)

sine = Sine(period=sample_rate / 440)

main_block += sine

write(
    main_block,
    os.path.join("out", "sine.wav"),
    sample_rate=sample_rate,
)
