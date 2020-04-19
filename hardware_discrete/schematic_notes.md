
# Schematic notes


T1 (power supply) Screw terminal connectors Left to Right:

| L | N | GND | V2 | COM | V1 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Signal Descriptions:

| Name | Description |
| --- | --- |
| L | Mains input live (black or red) |
| N | Mains input neutral (white) |
| GND | Mains input frame ground (green) |
| V2 | 12V supply output |
| COM | supply output common ground |
| V1 | 5V supply output |

MCU1 (Raspberry Pi) GPIO pin usage:

| Pin Number | Description |
| --- | --- |
|  2  | +5V (suggest use along with 4) |
|  4  | +5V (suggest use along with 2) |
|  6  | GND |
| 8-14 | (unused) |
| 16 | GPIO16 - assert high when authorized user scans card |

**NOTE** Pins 2,4 required for direct wire connection to power supply T1.  Pins 2,4 may be left unused if one supplies power to the Raspberry Pi via the micro-USB port.

MCU2 (Arduino) connection points:

| Pin ID | Description |
| --- | --- |
| VIN | Power supply in (regulated 5V) |
| GND | Ground |
| D13 | integrated LED |
| D5  | unlock pin (assert high) |
| D4  | accept pin (assert high) from RPi |

**NOTE** : The VIN pin required for connection to power supply T1.  The VIN pin may be unused if Arduino is powered by USB or barrel connector

RLY1 (Beefcake Relay Control Kit) connection points:

Low-voltage (smaller, black) terminal block:

| Pin Name | Description |
| --- | --- |
| 5V | Power input (5V) |
| CTRL | relay control signal |
| GND | Ground |

High-voltage (larger, blue) connection points:

| Pin Name | Description |
| --- | --- |
| NC | Relay Normally Closed contact |
| NO | Relay Normally Open contact |
| COM | Relay common contact |

PCB2 (MOSFET Power Control Kit) connection points:

System (3-terminal) connector:

| Pin Name | Description |
| --- | --- |
| C | Control signal |
| - | Ground rail |
| + | Power (5V) rail |

Device (2-terminal) connector:
| Pin Name | Description |
| --- | --- |
| + | connect to controlled device |
| - | connect to ground |
