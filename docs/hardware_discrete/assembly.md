
# Hardware Assembly Instructions

## Overview

* Initial Unit Assembly and test
  * RFID Reader (U1, PCB1)
  * Beefcake Relay Control Kit (RLY1)
  * MOSFET Power Control Kit (PCB2)
  * Power Supply (T1)
* Program and Configure Arduino (MCU2)
  * Firmware loading with Arduino IDE
  * Unit Testing the Arduino
* Program and Configure Raspberry Pi (MCU1)
  * Initial image installation
  * Prepare for configuration (SSH)
  * Configure and Install with Ansible
  * Unit Testing Raspberry Pi
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

## Arduino Setup

* To program the Arduino (Uno R3) use the Arduino IDE to upload the sketch [`arduino/sketches/doorproto_v6_control`](arduino/sketches/doorproto_v6_control/doorproto_v6_control.ino) onto an Arduino Uno R3 or other compatible board.

To test the programmed board one can do the following:

* Connect D4 to +5V ("accept" input from the Raspberry Pi)
* Ground D2 (the door button switch input line)

In either case D5 should raise to +5V for five seconds and D2 should flash for the same period of time.

## Assemble Test Circuit

Begin assembly by assembling the circuit per the [test circuit schematic](figures/discrete_arduino_test_ckt_202004302058.pdf).
This broadly involes the following steps:

* wiring the Arduino to the power supply
* connecting the exit button switch and LED.
* Connect Arduino pin D5 to an LED and resistor to ground instead of to the relay RLY1.
* Connect Arduino pin D4 directly to ground.  This emulates the presence of Raspberry Pi GPIO output 16, which pulls D4 low.

This leave MCU1 (the Raspberry Pi) and PCB1 (the RFID reader) unconnected,
but the circuit still can be tested in one of two ways:

* Press the exit button.  The LED on the button will light and the test LED wired to D5 will also light indicating that the relay control line has been activated.

* Disconnect Arduino pin D4 from ground.  This emulates the Raspberry Pi pulling GPIO 16 high when an authorized card has been scanned.

In either case, the exit button LED should light along with the LED connected to Arduino pin D4.

## Add Relay Connections (Optional)

A further incremental assembly may be performed at this point by adding the relay and connecting the magnetic lock and electric strike.  This is basically the complete assembled circuit minus MCU1 and PCB1.  One may consult the [full circuit schematic](figures/discrete_hardware_202004302058.pdf) as a reference.

To complete this partial assembly or the assembly of the full circuit one should make sure the ground connection to Arduino pin D4 is removed or it will interfere with relay control.  The test LED connected to pin D5 may be left in place if so desired, but it will be redundant with the LED installed on the RLY1 board.

## Raspberry Pi Setup

To set up the Raspberry Pi please follow the instructions in the [Raspberry Pi Readme](docs/rpi_software/README.md) in the `docs/rpi_software`
directory.

To test the Raspbery Pi software two options are available.  One option is to
hook up the RFID reader using a USB cable and use a card to trigger the reader.
The other option is to connect an Arduino loaded with the test sketch [`hodor_inputmocker`](../../arduino/sketches/hodor_inputmocker).  For details on this option consult the
[Arduino README](../../arduino/README.md).

To monitor the response of the Raspberry Pi several options exist.

* GPIO pin 16 should strobe high
* Event files should be written to the directory `/home/pi/hodor/events`.

## Full Circuit Assembly

Once the Raspberry Pi is tested one can connect GPIO 16 to Arduino pin D4 and connect PCB1 to the Raspberry Pi via a USB cable.  If one did the test circuit assembly described previously make sure the direct ground connection to Arduino D4 is removed otherwise it will interfere with relay control.

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
