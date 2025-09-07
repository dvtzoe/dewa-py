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
    An example demonstrating the use of the vibe-dewa synthesizer library.
    """
    # Global settings
    sample_rate = 48000
    output_folder = "out"
    os.makedirs(output_folder, exist_ok=True)

    # 1. Create a main canvas block of 20 seconds.
    main_block = Block(duration_seconds=20.0, sample_rate=sample_rate)
    print("Created a 20-second main block.")

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

        # Create a repeated version of the imported block
        repeated_block = imported_block.repeat(3)
        main_block.mount(repeated_block, at_time=9.0)

    # 3. Create an LFO for frequency modulation.
    lfo_fm = Block(duration_seconds=1.0, sample_rate=sample_rate)
    lfo_fm += Sine(5)  # 5 Hz sine wave LFO
    lfo_fm *= LinearRamp(start=50, end=0)  # Modulate frequency by 50 Hz decreasing to 0

    # 4. Demonstrate Square wave with FM.
    fm_square_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    fm_square_note += Square(440 + lfo_fm)  # Base frequency 440Hz modulated by LFO
    fm_square_note *= LinearRamp(start=1.0, end=0.0)
    main_block.mount(fm_square_note, at_time=13.0)
    print("Created a 1-second 440 Hz square wave note with FM.")

    # 5. Demonstrate Sawtooth wave with FM.
    fm_sawtooth_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    fm_sawtooth_note += Sawtooth(220 + lfo_fm)  # Base frequency 220Hz modulated by LFO
    fm_sawtooth_note *= LinearRamp(start=1.0, end=0.0)
    main_block.mount(fm_sawtooth_note, at_time=15.0)
    print("Created a 1-second 220 Hz sawtooth wave note with FM.")

    # 6. Demonstrate Triangle wave with FM.
    fm_triangle_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    fm_triangle_note += Triangle(330 + lfo_fm)  # Base frequency 330Hz modulated by LFO
    fm_triangle_note *= LinearRamp(start=1.0, end=0.0)
    main_block.mount(fm_triangle_note, at_time=17.0)
    print("Created a 1-second 330 Hz triangle wave note with FM.")

    # 7. Save the final audio to a file.
    output_filename = os.path.join(output_folder, "output-ai-6.mp3")
    write(main_block, output_filename, sample_rate=sample_rate)
    print(f"Successfully saved the final audio to '{output_filename}'.")
    print(f"You can now listen to the {output_filename} file.")


if __name__ == "__main__":
    main()
