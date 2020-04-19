
# Hardware Assembly Instructions

## Overview

* Initial Unit Assembly and test
  * RFID Reader (U1, PCB1)
  * Beefcake Relay Control Kit (RLY1)
  * MOSFET Power Control Kit (PCB2)
* Program and Configure MCUs
  * Raspberry Pi (MCU1)
  * Arduino Uno R3 (MCU2)
* Breadboard Assembly and Test
1. Assemble Units
1. RFID reader test
2. PCB1 (Beefcake Relay Control Kit)
1. Power supply assembly and test

## Initial Assembly and Test

### RFID Reader

Components:
* U1
* PCB1
* Mini-USB cable ("A" male to "mini-B" male)

Seat the RFID chip (U1) into the in-line sockets on the RFID reader (PCB1).
Make sure that the chip is properly aligned so that all the pins are
properly seated in the sockets.

To test the reader, plug the USB cable into the RFID reader and connect the
other end to a PC running a terminal monitor program.  When one places an
RFID card close to the RFID reader chip (an inch or so or closer) the reader
should beep and a line of twelve hexadecimal characters should appear on
the serial port monitor.

### Beefcake Relay Control Kit (RLY1)

Assemble the kit per Sparkfun instructions.  A basic test of the relay is
to use a multimeter or ohmmeter to confirm continuity between the NC and COM
terminals by default, and that continuity can be achieved when the 5V and GND
terminals are powered and a logic high signal is applied to the CTRL terminal.

### MOSFET Power Control Kit (PCB2)

Assemble the kit per Sparkfun instructions.  To test the MOSFET, use an ohmmeter
to confirm that resistance is high (>1MOhm) between the "+" and "-" terminals
on the "Device" side of the unit, and the resistance drops when the "System"
side is powered and a logic high voltage is applied to the "C" terminal.

## Appendix

### Monitor USB Port

Numerous options to exist for monitoring serial ports in various operating
systems, too many to detail here.  For the reader's convenience, a selection
of references to some how-to articles follow:

Windows:

  https://docs.microsoft.com/en-us/sysinternals/downloads/portmon

  http://www.serial-port-monitor.com/

Mac OS X:

  https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux

  https://www.virtual-serial-port.org/articles/serial-port-monitor-mac/

Linux:

  https://www.virtual-serial-port.org/articles/serial-port-monitor-linux/

  https://serverfault.com/questions/112957/sniff-serial-port-on-linux