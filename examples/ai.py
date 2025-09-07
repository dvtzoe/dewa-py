import os

from dewa import (
    Block,
    LinearRamp,
    Square,
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


if __name__ == "__main__":
    main()
