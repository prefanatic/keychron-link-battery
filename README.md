# Keychron Link battery extension

This experimental patch adds battery reports through Keychron Link for the **Keychron V1 Max ANSI encoder**.
The tested keyboard is V1M-D4, with USB ID `3434:0913`.
The tested receiver has USB ID `3434:d031`.
The keyboard can keep its existing 2.4 GHz connection.

The patch enables the existing wireless raw-HID dispatcher and corrects its misspelled build guard.
It adds an `A4` battery query and advertises that query through `A2`.
The response uses the keyboard's measured percentage, voltage, and charge state.
The firmware sends responses to queries; it does not send battery events without a query.

## Status

One keyboard passed the hardware test on 2026-10-10.
The keyboard reported 97% with its cable disconnected.
The user confirmed normal keys, receiver input, and the encoder.
The test required no receiver or wireless module update.
Other models and transports have no hardware verification.

The files came from the Chargewise workspace.
Chargewise retains its Rust adapter; this repository owns the firmware patch and build procedure.
See [the protocol](docs/protocol.md), [hardware evidence](docs/hardware-test.md), and [the firmware procedure](docs/firmware.md).
See [GitHub repository](docs/github.md) for the remote and visibility.

## Build

Use Linux with Git, GNU Make, Python 3, the Arm embedded toolchain, and `dfu-suffix`.
The original image used Arm GNU 13.2.Rel1.
Other compiler versions can produce different image hashes.
QMK also embeds the build time, so a new build changes the image hash.

Prepare the pinned source:

```sh
sh scripts/prepare-source.sh
python3 -m venv .venv
.venv/bin/python -m pip install -r .build/source/requirements.txt
```

Build the image:

```sh
PATH="$PWD/.venv/bin:$PATH" sh scripts/build.sh
python3 scripts/check.py
```

The script writes `.build/v1-max-ansi-battery-experimental.bin`.
The script does not write to a device.
The build uses the revision and target from [the manifest](firmware/manifest.json).
Git submodule revisions come from that upstream revision.
The build script rejects source changes that differ from the patch.

The original local images remain under `firmware/`.
Git excludes binary images and private backups.
The manifest preserves their hashes and the official recovery URL.

## Checks

```sh
python3 scripts/check.py
sh -n scripts/prepare-source.sh scripts/build.sh
```

The check validates the manifest, patch scope, and available image hashes and DFU suffixes.
GitHub CI also applies the patch to the pinned source and builds the keyboard target.
CI cannot verify hardware behavior.

## License and sources

The patch and scripts use **GPL-2.0-or-later**, consistent with the modified Keychron source files.
The upstream copyright notices remain intact.
The [LICENSE](LICENSE) contains the GPL version 2 text.
The official recovery image remains a local recovery file; this repository does not publish it.

- [Pinned Keychron source](https://github.com/Keychron/qmk_firmware/tree/c5d998442710b38650903937249144a0cd728ebe).
- [Community K8 HE extension reference](https://github.com/shayangohar/keychron-tray-widget/blob/master/firmware/keychron-k8-he-battery-wired.patch).

The community extension targets a different keyboard.
This project has no affiliation with Keychron.
