
# Hardware Setup - DRAFT - IN DEVELOPMENT

Updated: 2020-04-19

This directory contains information about constructing the hardware
supported by the door controller.

**WARNING** : This controller is not intended to be a complete
solution for building access control.  The onus is upon
implementers to ensure that this system is deployed in a manner
that does not violate any local building safety codes.  Improper
implementation of this system can leave a person trapped and
unable to exit a building which can result in injury or death
in an emergency situation.  Implementers are urged strongly to
exercise caution.

## Overview of Directory Contents

* `README.md` - this file
* [`assembly.md`](assembly.md) - assembly instructions
* [`BOM.md`](BOM.md) - Bill of Materials
* [`schematic_notes.md`](schematic_notes.md) - summary of component connections
* [`figures`](figures) - directory of figures including wiring diagram

## Access Control Overview

Bridgewire manages access to the shop with the assistance of an
access control system relying upon RFID cards.  Shop users are
granted an RFID card to permit access to the shop when open
shop nights or other scheduled events are conducted.  This card
functions as an electronic key allowing shop access to be managed
even when the building is unattended without having to require
the distribution of physical keys.

### The Shop Door

The shop door includes a traditional door entry handle with a keyed
tumbler lock as well as a deadbolt.  Both of these mechanisms work
in the traditional manner providing a baseline level of building
security, and provide a fallback in situations when building power
is unavailable.  As the keys for these locks are unavailable to
most Bridgewire members, the deadbolt is only used in situations
when either the controller system is unavailable or in emergency
situations or other occasions when the shop must be closed to the
general membership.

The door controller system supplements the door with several features.
A junction box has been placed by the door exterior to house an RFID
card reader.  The RFID reader lets users identify themselves in order
to gain access to the shop.  Further, the door is modified with
two separate locks to enforce access control that operate over and
above the traditional handle lock and deadbolt.  One is an electric
strike mounted into the door jamb and the other is an
electromagnetic lock mounted inside the door.  Both of these locks
are actuated by the electronic door controller.  

Additionally, as the magnetic lock must be disengaged in order to
permit users inside the building to exit the building, an exit
button is integrated into the controller and mounted next to the
door interior which users wishing to leave press to disengage the
magnetic lock.  When the button is pressed, the magnetic lock is
disengaged and the electric strike is engaged for five seconds
temporarily permitting users to exit.  The button includes an
LED which flashes while the door is unlocked providing some feedback
to the user.

### The Door Controller

The door controller includes Raspberry Pi computer to read the
RFID cards and an Arduino microcontroller to help actuate the
hardware.  Previous versions of the system had the Raspberry
Pi assume all hardware functions but the Arduino was included
to support new features under discussion by Bridgewire members.

The Raspberry Pi includes two programs to support access control.
The primary program is `watcher.py` which reads an access list
file and triggers the lock release when recognized RFID card
ID's are read.  A secondary program `hodor_slacker.py` is an
optional supplemental program that announces door events on a
designated Slack channel.

The Raspberry Pi does not directly release the locks but relies
upon the Arduino to manage this.  The Arduino uses a simple
firmware program which actuates the lock relay when given a
signal either by the Raspberry Pi or when the exit button is
pressed.

### Harware Features

**RFID Card Reader** - The RFID card reader is part of the door
controller's access control mechanism.  A junction box on the building
exterior by the door houses the card reader.  Users present their cards
to the box and the reader reads the ID and emits an audible beep to
provide feedback to the user.

**Electric Strike** - A normally-closed electric strike lock
mounted in the door jamb is one of two additional system-controlled
locks used to enforce access control over and above the door's
traditional doorknob and deadbolt.  The electric strike replaces
the traditional fixed strike plate in the door jamb to hold the
door's latch bolt closed.  Normally the strike is inert and functions
passively like a traditional fixed strike plate trapping the latch
bolt in the door jamb. When access is permitted a solenoid in the
electric strike releases a latch allowing the latch bolt to move
past the electric strike without unlocking the door.  Thus when the
door's deadbolt is not used the door can be locked to the general
public while allowing recognized RFID card holders to enter the
building.

**Magnetic Lock** - A magnetic lock mounted on the inside door jamb
supplements the electric strike to enforce access control.  This is
a secondary lock to provide added protection against attempts to
forcibly enter the building by defeating the door latch using a shim
or other mechanical means when the door's deadbolt is not in use.
An electromagnet is continuously energized causing it to hold a
ferromagnetic plate mounted to the door.  When access is permitted
power is removed from the electromagnet allowing the door to be
opened

**Exit Button** - The button triggers a one-shot timer to allow users
to use the exit without having to continuously hold down the button.
This improves accessibility and safety for using the exit.  The button
also includes an LED for user feedback and flashes when pressed.
