
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

MCU2 (Arduino) connection points:

| Pin ID | Description |
| --- | --- |
| D13 | integrated LED |
| D5  | unlock pin (assert high) |
| D4  | accept pin (assert high) from RPi |
