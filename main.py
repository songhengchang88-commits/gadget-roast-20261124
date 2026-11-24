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

