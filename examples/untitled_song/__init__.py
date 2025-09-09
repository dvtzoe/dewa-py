import os

from dewa import Block, LinearRamp, Sine
from dewa.io import write


def main():
    """
    Play "Daisy Bell" (A Bicycle Built for Two) using the dewa synthesizer library.
    """
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
        ("G4", 0.5),
        ("A4", 0.5),
        ("B4", 1.0),
        ("C5", 1.0),  # Dai-sy, Dai-sy
        ("B4", 0.5),
        ("A4", 0.5),
        ("G4", 1.5),
        ("G4", 0.5),  # Give me your an-
        ("A4", 0.5),
        ("B4", 0.5),
        ("C5", 1.0),
        ("D5", 1.0),  # swer do
        ("C5", 0.5),
        ("B4", 0.5),
        ("A4", 2.0),  # true
        ("G4", 0.5),
        ("A4", 0.5),
        ("B4", 1.0),
        ("C5", 1.0),  # I'm half cra-
        ("B4", 0.5),
        ("A4", 0.5),
        ("G4", 1.5),
        ("G4", 0.5),  # zy all for the
        ("A4", 0.5),
        ("B4", 0.5),
        ("C5", 1.0),
        ("D5", 1.0),  # love of you
        ("C5", 0.5),
        ("B4", 0.5),
        ("G4", 2.0),  #
        ("E5", 1.0),
        ("D5", 0.5),
        ("C5", 0.5),
        ("B4", 1.0),  # It won't be a
        ("A4", 1.0),
        ("G4", 0.5),
        ("A4", 0.5),
        ("B4", 1.0),  # stylish mar-riage
        ("C5", 1.0),
        ("B4", 0.5),
        ("A4", 0.5),
        ("G4", 1.0),  # I can't af-ford
        ("F4", 1.0),
        ("E4", 2.0),  # a carriage
        ("G4", 0.5),
        ("A4", 0.5),
        ("B4", 1.0),
        ("C5", 1.0),  # But you'll look
        ("D5", 0.5),
        ("C5", 0.5),
        ("B4", 1.5),
        ("B4", 0.5),  # sweet upon the
        ("C5", 0.5),
        ("D5", 0.5),
        ("E5", 1.0),
        ("D5", 1.0),  # seat of a bi-
        ("C5", 1.0),
        ("G4", 2.0),  # cycle built for two
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

            # # Apply envelope (fade in and out)
            # envelope = LinearRamp(start=0.0, end=0.3)
            # if note_duration_seconds > 0.2:
            #     # For longer notes, add a fade out
            #     fade_out_start = int(note_samples * 0.7)
            #     fade_out = LinearRamp(start=0.3, end=0.0)
            #     fade_out_block = Block(duration=note_samples - fade_out_start)
            #     fade_out_block += fade_out
            #
            #     # Apply fade in to first part
            #     fade_in_block = Block(duration=fade_out_start)
            #     fade_in_block += envelope
            #     note_block *= fade_in_block
            #
            #     # Apply fade out to last part
            #     note_block.samples[fade_out_start:] *= fade_out_block.samples
            # else:
            #     # For short notes, just apply envelope
            #     note_block *= envelope

            # Mount the note to the main block
            mount_point = int(current_time * sample_rate)
            main_block.mount(note_block, mount_point=mount_point)

        current_time += duration * beat_duration

    # Add some harmonics for richer sound
    # harmony_block = Block(duration=int(total_duration * sample_rate))
    # current_time = 0.0
    # for note_name, duration in melody:
    #     if note_name in notes:
    #         period = notes[note_name]
    #         note_duration_seconds = duration * beat_duration
    #         note_samples = int(note_duration_seconds * sample_rate)
    #
    #         # Create harmony note (fifth above)
    #         harmony_freq = period * 1.5  # Perfect fifth
    #         harmony_note = Block(duration=note_samples)
    #         harmony_note += Sine(harmony_freq)
    #
    #         # Lower volume for harmony
    #         harmony_note *= LinearRamp(start=0.0, end=0.15)
    #
    #         # Mount harmony
    #         mount_point = int(current_time * sample_rate)
    #         harmony_block.mount(harmony_note, mount_point=mount_point)
    #
    #     current_time += duration * beat_duration
    #
    # # Combine melody and harmony
    # main_block.mount(harmony_block, mount_point=0)

    # Write to file
    output_path = os.path.join(output_folder, "daisy_bell.wav")
    write(main_block, output_path, sample_rate=sample_rate)
    print(f"Daisy Bell melody saved to {output_path}")


if __name__ == "__main__":
    main()
