import os

from dewa import Block, Square
from dewa.io import write

sample_rate = 48000

main_block = Block(duration=5 * sample_rate)

square = Square(period=sample_rate / 440)

main_block += square

write(
    main_block,
    os.path.join("out", "square.wav"),
    sample_rate=sample_rate,
)
