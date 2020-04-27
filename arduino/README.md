
# Arduino Sketches

This directory contains several sketches used by the door controller.

* `doorproto_v6_control` - Control program used by the controller Arduino
(MCU2).
* `doorproto_relayblink` - Test program to flash the "unlock" output
on the Arduino (D5)
* `hodor_inputmocker` - Arduino sketch that can be used for functional
testing of the Raspberry Pi software

To use the test software `hodor_inputmocker` load the sketch onto an Arduino
and hook the Arduino the the USB RFID reader (PCB1) as follows:

| Arduino | USB RFID Reader |
| --- | --- |
| D1 (TX) | TX |
| GND | GND |

The sketch emits a byte sequence similar to the codes scanned by the RFID
reader at the rate of one code every ten seconds.  It cycles through a
fixed sequence of sixteen codes:

* `000000000000`
* `111111111111`
* `222222222222`
* `333333333333`
* `444444444444`
* `555555555555`
* `666666666666`
* `777777777777`
* `888888888888`
* `999999999999`
* `AAAAAAAAAAAA`
* `BBBBBBBBBBBB`
* `CCCCCCCCCCCC`
* `DDDDDDDDDDDD`
* `EEEEEEEEEEEE`
* `FFFFFFFFFFFF`
