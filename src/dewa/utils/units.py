def units(sample_rate: int, bpm: float) -> tuple[int, float, float]:
    """
    Returns a tuple of time units in seconds based on the given sample rate.

    Parameters:
        sample_rate: int => The sample rate in Hz.
    Returns:
        A tuple containing
        - Second: float => Duration of one second in samples.
        - Hz: float => Duration of one Hertz in samples.
        - Beat: float => Duration of one beat in samples (based on bpm).


    """
    return (
        sample_rate,  # Second
        1 / sample_rate,  # Hz
        60 / bpm * sample_rate,  # Beat
    )
