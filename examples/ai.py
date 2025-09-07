from dewa import (
    Block,
    LinearRamp,
    Sawtooth,
    Sine,
    Square,
    Triangle,
    write,
)


def main():
    """
    An example demonstrating the use of the vibe-dewa synthesizer library.
    """
    # Global settings
    sample_rate = 44100

    # 1. Create a main canvas block of 5 seconds.
    main_block = Block(duration_seconds=5.0, sample_rate=sample_rate)
    print("Created a 5-second main block.")

    # 2. Create the first note: A4 (440 Hz) for 1 second.
    note_a4 = Block(duration_seconds=1.0, sample_rate=sample_rate)
    note_a4 += Sine(440)

    # Apply a fade-out envelope to the note
    note_a4 *= LinearRamp(start=1.0, end=0.0)
    print("Created a 1-second 440 Hz note with a fade-out.")

    # 3. Create the second note: E5 (659.25 Hz) for 0.5 seconds.
    note_e5 = Block(duration_seconds=0.5, sample_rate=sample_rate)
    note_e5 += Sine(659.25)
    note_e5 *= LinearRamp(start=1.0, end=0.0)  # Also with a fade-out
    print("Created a 0.5-second 659.25 Hz note with a fade-out.")

    # 4. Create a vibrato (FM) effect.
    # A low-frequency oscillator (LFO) block of 1 second at 5 Hz
    lfo = Block(duration_seconds=1.0, sample_rate=sample_rate)
    lfo += Sine(5)
    lfo *= LinearRamp(20, 0)  # The vibrato depth will decrease over time

    # The carrier note that will be modulated
    carrier_note = Block(duration_seconds=1.0, sample_rate=sample_rate)
    # The frequency of the Sine modifier is the LFO block itself!
    carrier_note += Sine(440 + lfo)  # Base frequency of 440Hz modulated by the LFO
    carrier_note *= LinearRamp(1.0, 0.0)
    print("Created a 1-second note with a 5 Hz vibrato effect.")

    # 5. Create a square wave note.
    note_square = Block(duration_seconds=0.5, sample_rate=sample_rate)
    note_square += Square(220)
    note_square *= LinearRamp(start=1.0, end=0.0)
    print("Created a 0.5-second 220 Hz square wave note.")

    # 6. Create a sawtooth wave note.
    note_sawtooth = Block(duration_seconds=0.5, sample_rate=sample_rate)
    note_sawtooth += Sawtooth(220)
    note_sawtooth *= LinearRamp(start=1.0, end=0.0)
    print("Created a 0.5-second 220 Hz sawtooth wave note.")

    # 7. Create a triangle wave note.
    note_triangle = Block(duration_seconds=0.5, sample_rate=sample_rate)
    note_triangle += Triangle(220)
    note_triangle *= LinearRamp(start=1.0, end=0.0)
    print("Created a 0.5-second 220 Hz triangle wave note.")

    # 8. Mount the blocks onto the main canvas.
    main_block.mount(note_a4, at_time=0.0)
    main_block.mount(note_e5, at_time=1.0)
    main_block.mount(carrier_note, at_time=1.75)
    main_block.mount(note_square, at_time=3.0)
    main_block.mount(note_sawtooth, at_time=3.5)
    main_block.mount(note_triangle, at_time=4.0)
    print("Mounted all notes onto the main block.")

    # 9. Save the final audio to a file.
    output_filename = "output-ai.wav"
    write(main_block, output_filename)
    print(f"Successfully saved the final audio to '{output_filename}'.")
    print("You can now listen to the output-ai.wav file.")


if __name__ == "__main__":
    main()
