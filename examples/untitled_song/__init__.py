import os

from dewa import Block, Sine
from dewa.io import write


def main():
    # Global settings
    sample_rate = 48000
    output_folder = "out"
    os.makedirs(output_folder, exist_ok=True)

    # Note frequencies (in Hz)
    notes = {
        "C4": 261.63,
        "D4": 293.66,
        "E4": 329.63,
        "F4": 349.23,
        "G4": 392.00,
        "A4": 440.00,
        "B4": 493.88,
        "C5": 523.25,
        "D5": 587.33,
        "E5": 659.25,
        "F5": 698.46,
        "G5": 783.99,
        "A5": 880.00,
        "B5": 987.77,
        "C6": 1046.50,
    }

    # Daisy Bell melody (simplified version)
    # Each tuple is (note, duration_in_beats)
    melody = [
        ("G5", 0.5),
        ("A5", 0.5),
        ("G5", 0.5),
        ("F5", 0.5),
        ("E5", 0.5),
        ("F5", 0.5),
        ("G5", 0.5),
        ("D5", 0.5),
        ("E5", 0.5),
        ("F5", 0.5),
        ("E5", 0.5),
        ("F5", 0.5),
        ("G5", 0.5),
        ("G5", 0.5),
        ("A5", 0.5),
        ("G5", 0.5),
        ("F5", 0.5),
        ("E5", 0.5),
        ("F5", 0.5),
        ("G5", 0.5),
        ("D5", 0.5),
        ("G5", 0.5),
        ("E5", 0.5),
        ("C5", 0.5),
    ]

    # Create main block
    beat_duration = 0.6  # Duration of one beat in seconds
    total_duration = sum(duration for _, duration in melody) * beat_duration
    main_block = Block(duration=int(total_duration * sample_rate), dtype=float)

    # Generate melody
    current_time = 0.0
    for note_name, duration in melody:
        if note_name in notes:
            period = sample_rate / notes[note_name]
            note_duration_seconds = duration * beat_duration
            note_samples = int(note_duration_seconds * sample_rate)

            # Create note block
            note_block = Block(duration=note_samples)

            # Add sine wave for the note
            note_block += Sine(period)

            # Mount the note to the main block
            mount_point = int(current_time * sample_rate)
            main_block.mount(note_block, mount_point=mount_point)

        current_time += duration * beat_duration

    # Write to file
    output_path = os.path.join(output_folder, "song.wav")
    write(main_block, output_path, sample_rate=sample_rate)
    print(f"Song melody saved to {output_path}")


if __name__ == "__main__":
    main()
