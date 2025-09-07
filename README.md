# Dewa

Dewa is a simple (I hope) and flexible synthesizer library for Python. It allows you to create and manipulate audio signals using a block-based approach. You can generate various waveforms, apply modifiers, and even load external audio files.

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

## Installation

To use Dewa, you need to have `ffmpeg` installed on your system. You can install it using your system's package manager.

Then, you can install Dewa using `pip`:

```bash
pip install .
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


"""
An example demonstrating the use of the dewa synthesizer library.
"""
# Global settings
sample_rate = 48000
output_folder = "out"
os.makedirs(output_folder, exist_ok=True)

# 1. Create a main canvas block of 10 seconds.
main_block = Block(duration_seconds=10.0, sample_rate=sample_rate)
print("Created a 10-second main block.")

# 2. Load an external audio file.
input_audio_path = os.path.join(output_folder, "sample-3s.mp3")
if os.path.exists(input_audio_path):
    imported_block = from_file(input_audio_path, sample_rate=sample_rate)
    print(f"Loaded audio from '{input_audio_path}'.")
    main_block.mount(imported_block, at_time=0.0)

# 3. Create a square wave note.
note_square = Block(duration_seconds=0.5, sample_rate=sample_rate)
note_square += Square(440)
note_square *= LinearRamp(start=1.0, end=0.0)
print("Created a 0.5-second 440 Hz square wave note.")

# 4. Mount the blocks onto the main canvas.
main_block.mount(note_square, at_time=4.0)
print("Mounted all notes onto the main block.")

# 5. Save the final audio to a file.
output_filename = os.path.join(output_folder, "output-ai-3.mp3")
write(main_block, output_filename, sample_rate=sample_rate)
print(f"Successfully saved the final audio to '{output_filename}'.")
print(f"You can now listen to the {output_filename} file.")



```

## Modifiers

Dewa comes with a set of built-in modifiers that you can use to shape your audio signals. To use a modifier, you can simply add it to a `Block` object.

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

## Operations                                                                                                                                 │
### Reverse                                                                                                                                   │
                                                                                                                                              │
Reverses the audio block.                                                                                                                     │
                                                                                                                                              │
```python                                                                                                                                     │
reversed_block = block.reverse()                                                                                                              │
```                                                                                                                                           │
                                                                                                                                              │
### Invert                                                                                                                                    │
                                                                                                                                              │
Inverts the phase of the audio block.                                                                                                         │
                                                                                                                                              │
```python                                                                                                                                     │
inverted_block = -block                                                                                                                       │
```                                                                                                                                           │

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
