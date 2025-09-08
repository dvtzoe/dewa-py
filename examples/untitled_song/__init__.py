import os

from dewa import (
    Block,
    Echo,
    LinearRamp,
    RingMod,
    Sawtooth,
    Sine,
    Square,
    Tremolo,
    Triangle,
    from_file,
    write,
)

sample_rate = 48000

main_block = Block(sample_rate=sample_rate)

simple_sine = Sine(frequency=440)

idk = Block(duration=1, sample_rate=sample_rate)
idk += simple_sine
idk.repeat(3)

write(
    main_block,
    os.path.join("out", "output.wav"),
    sample_rate=sample_rate,
)
