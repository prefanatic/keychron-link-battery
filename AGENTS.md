# Firmware agent workflow

Read README.md, firmware/manifest.json, and docs/protocol.md before a change.
This repository owns the V1 Max patch, build scripts, and firmware documentation.
Chargewise owns the host adapter.

Keep the upstream source revision explicit.
Preserve the exact keyboard target and the protocol signature.
Do not extend support to another model without separate evidence.
Do not change the protocol without coordination with the host adapter.
Keep queries bounded in host tools.
Do not treat a receiver timeout as proof that firmware setup is necessary.

Run scripts/check.py after a change.
Run shell syntax checks after a script change.
Build the target after a patch change.
Record compiler versions and hardware test limits.
Do not put device serials, macros, keymaps, or private backups in Git.
Keep images and build outputs outside Git.

A code change does not authorize a firmware write.
Obtain explicit authorization before a device write, bootloader action, or permission change.
Do not commit, push, reset, or discard changes without explicit approval.
