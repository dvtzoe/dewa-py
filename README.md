# Dewa

Dewa is a simple and flexible synthesizer library for Python. It allows you to create and manipulate audio signals using a block-based approach. You can generate various waveforms, apply modifiers, and even load external audio files.

## Features

*   Block-based audio synthesis.
*   A variety of built-in modifiers:
    *   `Sine`
    *   `Square`
    *   `Sawtooth`
    *   `Triangle`
    *   `LinearRamp`
*   Load audio from any format supported by ffmpeg.
*   Export audio to any format supported by ffmpeg.
*   Reverse and invert audio blocks.
*   Frequency modulation for wave modifiers.

## Installation

To use Dewa, you need to have `ffmpeg` installed on your system. You can install it using your system's package manager.

Then, you can install Dewa using `uv`:

```bash
uv pip install .
```

## Usage

Here is a simple example of how to use Dewa to create a short audio clip:

```python
import os

from dewa import (
    Block,
    LinearRamp,
    Sawtooth,
    Sine,
    Square,
    Triangle,
    from_file,
    write,
)


def main():
    """
    An example demonstrating the use of the dewa synthesizer library.
    """
    # Global settings
    sample_rate = 48000
    output_folder = "out"
    os.makedirs(output_folder, exist_ok=True)

    # 1. Create a main canvas block of 15 seconds.
    main_block = Block(duration_seconds=15.0, sample_rate=sample_rate)
    print("Created a 15-second main block.")

    # 2. Load an external audio file.
    input_audio_path = os.path.join(output_folder, "sample-3s.mp3")
    if os.path.exists(input_audio_path):
        imported_block = from_file(input_audio_path, sample_rate=sample_rate)
        print(f"Loaded audio from '{input_audio_path}'.")
        main_block.mount(imported_block, at_time=0.0)

        # Create a reversed version of the imported block
        reversed_block = imported_block.reverse()
        main_block.mount(reversed_block, at_time=3.0)

        # Create an inverted version of the imported block
        inverted_block = -imported_block
        main_block.mount(inverted_block, at_time=6.0)

    # 3. Create an LFO for frequency modulation.
    lfo_fm = Block(duration_seconds=1.0, sample_rate=sample_rate)
    lfo_fm += Sine(5)  # 5 Hz sine wave LFO
    lfo_fm *= LinearRamp(start=50, end=0)  # Modulate frequency by 50 Hz decreasing to 0

    # 4. Demonstrate Square wave with FM.
    fm_square_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    fm_square_note += Square(440 + lfo_fm)  # Base frequency 440Hz modulated by LFO
    fm_square_note *= LinearRamp(start=1.0, end=0.0)
    main_block.mount(fm_square_note, at_time=9.0)
    print("Created a 1-second 440 Hz square wave note with FM.")

    # 5. Demonstrate Sawtooth wave with FM.
    fm_sawtooth_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    fm_sawtooth_note += Sawtooth(220 + lfo_fm)  # Base frequency 220Hz modulated by LFO
    fm_sawtooth_note *= LinearRamp(start=1.0, end=0.0)
    main_block.mount(fm_sawtooth_note, at_time=11.0)
    print("Created a 1-second 220 Hz sawtooth wave note with FM.")

    # 6. Demonstrate Triangle wave with FM.
    fm_triangle_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    fm_triangle_note += Triangle(330 + lfo_fm)  # Base frequency 330Hz modulated by LFO
    fm_triangle_note *= LinearRamp(start=1.0, end=0.0)
    main_block.mount(fm_triangle_note, at_time=13.0)
    print("Created a 1-second 330 Hz triangle wave note with FM.")

    # 7. Save the final audio to a file.
    output_filename = os.path.join(output_folder, "output-ai-5.mp3")
    write(main_block, output_filename, sample_rate=sample_rate)
    print(f"Successfully saved the final audio to '{output_filename}'.")
    print(f"You can now listen to the {output_filename} file.")


if __name__ == "__main__":
    main()

```

## Modifiers

Dewa comes with a set of built-in modifiers that you can use to shape your audio signals. To use a modifier, you can simply add it to a `Block` object.

### Frequency Modulation

All wave-generating modifiers (`Sine`, `Square`, `Sawtooth`, `Triangle`) support frequency modulation. You can pass a `Block` object as the `frequency` parameter to dynamically change the frequency over time.

```python
from dewa import Block, Sine, Square, LinearRamp

# Create an LFO (Low-Frequency Oscillator) to modulate the frequency
lfo = Block(duration_seconds=1.0, sample_rate=44100)
lfo += Sine(5)  # 5 Hz sine wave
lfo *= LinearRamp(start=100, end=0) # Modulate frequency by 100 Hz decreasing to 0

# Use the LFO to modulate the frequency of a Square wave
square_with_fm = Block(duration_seconds=1.0, sample_rate=44100)
square_with_fm += Square(440 + lfo) # Base frequency 440Hz modulated by LFO
```

### Sine

Generates a sine wave.

```python
block = Block(duration_seconds=1.0)
block += Sine(440) # 440 Hz sine wave
```

### Square

Generates a square wave.

```python
block = Block(duration_seconds=1.0)
block += Square(440) # 440 Hz square wave
```

### Sawtooth

Generates a sawtooth wave.

```python
block = Block(duration_seconds=1.0)
block += Sawtooth(440) # 440 Hz sawtooth wave
```

### Triangle

Generates a triangle wave.

```python
block = Block(duration_seconds=1.0)
block += Triangle(440) # 440 Hz triangle wave
```

### LinearRamp

Creates a linear ramp. This is useful for creating envelopes.

```python
block = Block(duration_seconds=1.0)
block += Sine(440)
block *= LinearRamp(start=1.0, end=0.0) # Fade out
```

## Operations

### Reverse

Reverses the audio block.

```python
reversed_block = block.reverse()
```

### Invert

Inverts the phase of the audio block.

```python
inverted_block = -block
```

## Loading Audio

You can load audio from any file format supported by ffmpeg using the `from_file` function.

```python
from dewa import from_file

block = from_file("my_audio.mp3")
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the GPL-3.0 License. See the `LICENSE` file for details.
