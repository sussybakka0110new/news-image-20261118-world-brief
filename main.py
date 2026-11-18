"""Copy the committed 18 November 2026 world-news poster into the output directory."""

import os
import shutil
import struct
from pathlib import Path

SOURCE = Path(__file__).resolve().with_name("entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_image() -> None:
    """Reject a truncated, non-PNG, or oversized poster before it is copied."""
    with SOURCE.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG")
    if len(header) < 24:
        raise SystemExit("entry.png has a truncated IHDR")
    width, height = struct.unpack(">II", header[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit("entry.png exceeds the 1024x1024 limit")


def main() -> None:
    """Place the poster where the grader reads it, with an intake size guard."""
    if not SOURCE.is_file():
        raise SystemExit("entry.png is missing from the repository")
    if SOURCE.stat().st_size > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB intake limit")
    check_image()
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out / "entry.png")


if __name__ == "__main__":
    main()
