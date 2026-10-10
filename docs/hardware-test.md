# Hardware evidence

The original test used one V1 Max ANSI encoder on 2026-10-10.
The keyboard model was V1M-D4, with USB ID `3434:0913`.
The Keychron Link receiver had USB ID `3434:d031`.
The receiver reported firmware `c.3.0 Jun 13 2024 10:28:05` and receiver protocol version 1.

Two complete reads of the original keyboard firmware version 1.1.2 matched.
The helper verified every written byte before the keyboard restarted.
The restored keymap, macros, encoder, layout, and lighting matched the saved settings.
The keyboard reported 97% through the receiver with its cable disconnected.
The user confirmed normal keyboard input and the encoder.
The receiver and wireless module required no update.

The manifest records image hashes and test results.
Private flash backups and keyboard settings remain outside this repository.
The official recovery image is version 1.1.1, not the private original version 1.1.2 backup.

A later cable test confirmed charge-state transitions through the receiver.
Chargewise stored each transition about 0.5 seconds after the USB event.
The user confirmed an immediate display change.
That result measures host response on this desktop; it does not establish a firmware timing guarantee.

Other keyboard variants, receiver `3434:d030`, Bluetooth, and direct USB battery queries have no hardware verification.

## Repository move verification

The separate repository passed an isolated build on 2026-10-10 with Arm GNU 13.2.Rel1.
The original image and the new image each contain 108256 bytes.
Only the embedded build time and the DFU CRC differ.
Both local image hashes match their original manifest entries.
The new image passed the DFU suffix and CRC checks.
The source-only repository check passed without local binary images.
The check rejected an image with a corrupt byte.
Chargewise passed its formatter, analyzer, and all 48 tests after the reference update.
This verification did not write firmware or test the new image on hardware.
The GitHub workflow awaits the first push.
