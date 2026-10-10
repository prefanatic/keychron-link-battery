#!/usr/bin/env python3
"""Validate repository files without device access."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PATCH_PATHS = {
    "keyboards/keychron/common/keychron_raw_hid.c",
    "keyboards/keychron/common/wireless/wireless.c",
    "keyboards/keychron/v1_max/rules.mk",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_suffix(path: Path) -> None:
    data = path.read_bytes()
    require(len(data) >= 16, f"The image is too short: {path}")
    suffix = data[-16:]
    require(suffix[2:12] == bytes.fromhex("11df8304000155464410"),
            f"The DFU suffix is invalid: {path}")
    crc = zlib.crc32(data[:-4]) ^ 0xFFFFFFFF
    require(int.from_bytes(suffix[12:], "little") == crc,
            f"The DFU CRC is invalid: {path}")


def check_source(source: Path, manifest: dict, patch: bytes) -> None:
    def git(*args: str) -> bytes:
        return subprocess.check_output(["git", "-C", str(source), *args])

    require(git("rev-parse", "HEAD").decode().strip() == manifest["revision"],
            "The source revision differs from the manifest.")
    diff = git("diff", "--no-ext-diff", "--binary", "--abbrev=7", "HEAD")
    require(diff == patch, "The source changes differ from the exact firmware patch.")
    subprocess.run(["git", "-C", str(source), "apply", "--reverse", "--check",
                    str(ROOT / "firmware" / manifest["patch"])], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "firmware/manifest.json").read_text())
    require(re.fullmatch(r"[0-9a-f]{40}", manifest["revision"]) is not None,
            "The source revision must contain 40 hexadecimal characters.")
    require(manifest["target"] == "keychron/v1_max/ansi_encoder:keychron",
            "The keyboard target differs from the verified target.")
    require(manifest["usb_id"] == "3434:0913", "The keyboard identity is invalid.")
    patch_path = ROOT / "firmware" / manifest["patch"]
    patch = patch_path.read_bytes()
    paths = re.findall(rb"^diff --git a/(\S+) b/(\S+)$", patch, re.MULTILINE)
    require(len(paths) == 3 and all(a == b for a, b in paths)
            and {a.decode() for a, _ in paths} == PATCH_PATHS,
            "The patch changes files outside its declared scope.")
    require(hashlib.sha256(patch).hexdigest() == manifest["patch_sha256"],
            "The patch hash differs from the manifest.")
    for key in ("image", "recovery"):
        entry = manifest[key]
        require(re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                f"The {key} hash is invalid.")
        path = ROOT / "firmware" / entry["filename"]
        if path.exists():
            require(hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"],
                    f"The image hash differs from the manifest: {path}")
            if "size" in entry:
                require(path.stat().st_size == entry["size"], "The image size is invalid.")
            check_suffix(path)
    built = ROOT / ".build/v1-max-ansi-battery-experimental.bin"
    if built.exists():
        check_suffix(built)
    if args.source is not None:
        check_source(args.source, manifest, patch)
    print("Repository checks passed.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"Check failed: {error}", file=sys.stderr)
        sys.exit(1)
