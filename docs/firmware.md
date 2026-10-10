# Firmware procedure

The original image is `firmware/v1-max-ansi-battery-experimental.bin`.
The build script writes a new image under `.build/`.
The official recovery image is `firmware/v1-max-ansi-official-1.1.1.bin`.
The manifest records the SHA-256 values for both files.
The firmware build and DFU suffix check passed.
The hardware test passed on one keyboard.
Two complete reads of the original 1.1.2 flash matched.
Every written byte passed verification before the keyboard restarted.
The keymap, macros, encoder, layout, and lighting matched the saved settings after restoration.

The test requires explicit approval before any firmware write.
Connect the exact V1 Max ANSI encoder keyboard by USB.
Confirm USB ID `3434:0913` before you enter its bootloader.
Export its keymap and macros through Keychron Launcher.
Close applications that use its raw-HID interface.
Prepare another input device before you enter the bootloader.
Obtain administrator access while the keyboard can still type.
Save two complete reads of the original flash before a firmware write.
Confirm that both reads match.
The original test read 262144 bytes from address `0x08000000`.
Keep those backups and your keyboard settings outside this repository.
Use the V1 Max manual to enter its STM32 bootloader.
Confirm that only the intended keyboard appears as DFU device `0483:df11`.
The DFU identity identifies the chip, not the keyboard model.
The private helper from the original test is not part of this repository.
It used local device paths and private settings backups.

The following command writes the experimental image after those checks:

```sh
dfu-util -d 0483:df11 -a 0 -s 0x08000000:leave -D firmware/v1-max-ansi-battery-experimental.bin
```

Reconnect the keyboard after the write completes.
Set the switch to **G** to test the receiver connection.
Chargewise must receive a valid battery report before it confirms support.
This test does not update the receiver or wireless module.
A missing response can indicate incompatible wireless firmware.
The official wireless updater requires Windows.
A separate update would require a separate review and approval.

Use the same bootloader procedure to restore the official image if the test fails:

```sh
dfu-util -d 0483:df11 -a 0 -s 0x08000000:leave -D firmware/v1-max-ansi-official-1.1.1.bin
```

Restore your exported settings after recovery if necessary.
The hardware test must confirm normal keys, the encoder, receiver input, and battery data.
The tested keyboard passed those checks.
The application still requires an exact model check and approval for each firmware installation.
