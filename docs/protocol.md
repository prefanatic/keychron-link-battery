# Battery protocol version 1

The vendor raw-HID interface uses usage page `FF60` and 32-byte packets.
Use the receiver identity query `B2` before a keyboard query.
The tested receiver reports vendor `3434`, product `0913`, and connection state 1.
The host must serialize transactions on the same receiver.
Chargewise uses a receiver lock and a 500 ms limit for each reply.

## Capability

Send `A2` with the remaining bytes set to zero.
Require a 32-byte reply with byte 0 equal to `A2` and byte 1 equal to zero.
The battery extension sets mask `04` in reply byte 3.
Send `A4` only after that capability check succeeds.
A timeout alone does not establish that the extension is absent.

## Battery query

Send `A4` with the remaining bytes set to zero.
Byte offsets below refer to the 32-byte reply.

| Offset | Field | Value |
| --- | --- | --- |
| 0 | Command | `A4` |
| 1 | Percentage | 0–100 |
| 2–3 | Voltage | Millivolts, little-endian |
| 4 | Charge state | 0: no charge; 1: charge active; 2: charge complete |
| 5 | Transport | 4 for the tested 2.4 GHz connection |
| 6 | Model | 1 for this V1 Max extension |
| 7–8 | Signature | ASCII `CW` |
| 9 | Protocol version | 1 |
| 10–31 | Reserved | Zero |

Chargewise requires model 1, signature `CW`, version 1, and transport 4.
It accepts voltage values from 2500 to 4500 mV.
It rejects invalid lengths, percentages, charge states, and signatures.
The firmware obtains the percentage and voltage from the existing battery functions.
It obtains the charge state from USB power and the charge pin.
The protocol supplies no capacity, cycle count, or battery health field.

The firmware does not send unsolicited battery reports.
Chargewise queries every two seconds and also queries after relevant device events.
A transient missing reply must remain a missing sample.
The host can display an old sample with its age, but must exclude it from new history and predictions.
