import os

from dewa import Echo, from_file, write

sample_rate = 44100

main_block = from_file(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "samples", "metal_pipe.opus"
    )
)

echo_effect = Echo(delay=5000, decay=0.6)

main_block += echo_effect

write(
    main_block,
    os.path.join("out", "echo_output.wav"),
    sample_rate=sample_rate,
)
