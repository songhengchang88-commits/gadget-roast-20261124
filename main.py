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


def atomic_write(target_path: Path, content: str) -> None:
    """Write text atomically via temporary file and verify on-disk contents."""
    target_dir = target_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=target_dir,
        delete=False,
        prefix="entry_",
        suffix=".tmp",
    )
    temp_path = Path(temp_file.name)
    try:
        temp_file.write(content)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()

        temp_path.replace(target_path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    # Read the file back to verify the on-disk bytes decode to exactly what was validated
    with open(target_path, "rb") as f:
        disk_bytes = f.read()

    try:
        disk_decoded = disk_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        sys.stderr.write(f"Verification error: on-disk bytes failed UTF-8 decode: {exc}\n")
        sys.exit(1)

    if disk_decoded != content:
        sys.stderr.write("Verification error: on-disk content does not match validated text\n")
        sys.exit(1)


def main() -> None:
    """Entry point: validate roast text, write entry.txt atomically, and verify."""
    output_dir = resolve_output_dir()
    target_file = output_dir / "entry.txt"

    payload = ROAST_LINE + "\n"
    validated = validate_text(payload)
    atomic_write(target_file, validated)

    print(f"Wrote {target_file} ({len(validated)} code points)")


if __name__ == "__main__":
    main()



