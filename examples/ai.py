from dewa import Block, LinearRamp, Sine, write


def main():
    """
    An example demonstrating the use of the vibe-dewa synthesizer library.
    """
    # Global settings
    sample_rate = 44100

    # 1. Create a main canvas block of 3 seconds.
    main_block = Block(duration_seconds=3.0, sample_rate=sample_rate)
    print("Created a 3-second main block.")

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

    # 5. Mount the blocks onto the main canvas.
    main_block.mount(note_a4, at_time=0.0)
    main_block.mount(note_e5, at_time=1.0)
    main_block.mount(carrier_note, at_time=1.75)
    print("Mounted all notes onto the main block.")

    # 6. Save the final audio to a file.
    output_filename = "output.wav"
    write(note_a4, output_filename)
    print(f"Successfully saved the final audio to '{output_filename}'.")
    print("You can now listen to the output.wav file.")


if __name__ == "__main__":
    main()
