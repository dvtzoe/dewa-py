import argparse

from src._global import g
from src.main import main


def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="dewa", description="Waveform synthesizer CLI"
    )
    _ = parser.add_argument(
        "filename",
        type=str,
        help="Input file name",
    )
    _ = parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file name",
        default="output.wav",
    )
    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parsed = parser.parse_args()

    if not parsed.filename:  # pyright: ignore[reportAny]
        parser.print_help()
        return

    g.filename = parsed.filename  # pyright: ignore[reportAny]
    g.output = parsed.output  # pyright: ignore[reportAny]
    g.verbose = parsed.verbose  # pyright: ignore[reportAny]

    main()
