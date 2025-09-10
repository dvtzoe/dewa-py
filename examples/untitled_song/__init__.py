import os

import dewa as dw


def main():
    # Global settings
    sample_rate = 48000
    bpm = 100
    notes = dw.constants.notes
    s, Hz, beat = dw.utils.units(sample_rate, bpm)
    print(
        f"Sample Rate: {sample_rate} Hz, BPM: {bpm}, 1 beat = {beat:.2f} s, 1 s = {s} samples, 1 Hz = {Hz} samples"
    )

    output_folder = "out"
    os.makedirs(output_folder, exist_ok=True)

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
    main_block = dw.Block()

    # Generate melody
    for note_name, duration in melody:
        if note_name in notes:
            period = sample_rate / notes[note_name]
            note_samples = int(duration * beat)

            # Create note block
            note_block = dw.Block(duration=note_samples)

            # Add sine wave for the note
            note_block += dw.Sine(period)

            # Mount the note to the main block
            main_block.concat(note_block)

    # Write to file
    output_path = os.path.join(output_folder, "song.wav")
    dw.io.write(main_block, output_path, sample_rate=sample_rate)
    print(f"Song melody saved to {output_path}")


if __name__ == "__main__":
    main()
