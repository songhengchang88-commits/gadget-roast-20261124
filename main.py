"""Entrypoint for make.fun bounty: One-Line Roast: The Gadget You Use Every Day.

Repository anchor:
makefun anchor f9f22a90d1fca8229985884e00bd74bf781f3525 round 34236524
"""

import os
import sys
import tempfile
from pathlib import Path

ROAST_LINE = "1Password demands a 32-character master passphrase, two-factor authenticator, and a biometric retina scan to view a discount coupon for socks."


def resolve_output_dir() -> Path:
    """Resolve the output directory from $MAKEFUN_OUTPUT_DIR, falling back to /output and ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir and env_dir.strip():
        target = Path(env_dir.strip())
        target.mkdir(parents=True, exist_ok=True)
        return target

    # Fall back to /output
    default_dir = Path("/output")
    try:
        default_dir.mkdir(parents=True, exist_ok=True)
        probe = default_dir / ".probe_writable"
        probe.touch()
        probe.unlink()
        return default_dir
    except OSError:
        pass

    # Fall back to ./output
    fallback_dir = Path("./output").resolve()
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_dir


def validate_text(text: str) -> str:
    """Validate text strictly and fail loudly if invalid."""
    try:
        raw_bytes = text.encode("utf-8")
        decoded = raw_bytes.decode("utf-8")
    except UnicodeError as exc:
        sys.stderr.write(f"Validation error: text is not valid UTF-8: {exc}\n")
        sys.exit(1)

    codepoints = len(decoded)
    if codepoints < 1 or codepoints > 200:
        sys.stderr.write(
            f"Validation error: text length {codepoints} code points is not within 1 to 200 code points\n"
        )
        sys.exit(1)

    if not decoded.strip():
        sys.stderr.write("Validation error: text is only whitespace\n")
        sys.exit(1)

    return decoded


