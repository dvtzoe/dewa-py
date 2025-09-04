import numpy as np


# Make variables mutable
class Global:
    filename: str = str("")
    output: str = "output.wav"
    verbose: bool = False
    sample_rate: int = 44100
    data: np.ndarray = np.array([], dtype=np.float32)


g = Global()
