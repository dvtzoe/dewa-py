import os

from dewa import Block, Tremolo
from dewa.io import write

sample_rate = 48000

main_block = Block(duration=5 * sample_rate)

tremolo = Tremolo(sample_rate / 440, 0.5)

main_block += tremolo

write(
    main_block,
    os.path.join("out", "tremolo.wav"),
    sample_rate=sample_rate,
)
