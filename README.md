# hodor_picontroller

This repository contains code and support documents for Bridgewire's Raspberry Pi-based door controller.  There are many like it [see below](#Prior Art), but this one is Bridgewire's.  The materials below are related to an update of the controller providing access to Bridgewire's shop, based on an original design from a previous member.  This repository represents a proposed update both for the door's functionality and an enhancement of the controller's design documentation, including a bill of materials along with assembly and test instructions.  These materials are provided so that future maintainers may have resources to more easily maintain and extend the controller.

## Overview of Contents

* `deploy_ansible` - Scripts to install Hodor onto a Raspberry Pi using Ansible
* `docs` - documentation
* `extras` - random utility scripts
* `hodor_controller` - Door controller program
* `hodor_slackbot` - Monitor program communicating door accesses to Slack
* `hodor_slackbot_configfiles` - example configuration files
* `setup.py` - installation script for `hodor_controller` and `hodor_slackbot`
* `unit_test_suite.py` - test script for `hodor_controller` and `hodor_slackbot`

For information on the hardware, please see [hardware README](docs/hardware_discrete/README.md)
in the `docs/hardware_discrete` directory.

For information on the Raspberry Pi software, including the `hodor_watcher`
program in `hodor_controller` and the `hodor_slacker` program in
`hodor_slackbot` please consult the
[Raspberry Pi Readme](docs/rpi_software/README.md) in the `docs/rpi_software`
directory.

## Feature and Design Changes

The current version of the system described in this repository is different
from the current installed system at Bridgewire in several respects:

* The RFID reader connects to the Raspberry Pi by a USB cable interface
instead of a set of unshielded wires
* The button uses a one-shot timer and flashes an LED to make it easier
to exit the office
* The Raspberry Pi software installation has been updated to make it
easier to maintain and its installation has been automated

## Prior Art

As the original designer is out of contact, the precise provenance of the original design for Bridgewire's door controller is not known.  That said, other projects of a similar nature may be found on the web including:

* [Pi-Lock](http://www.pi-lock.com/)
* [Simple RFID Door Lock System](https://hackaday.com/2016/09/25/simple-rfid-door-lock-system/) on [Hackaday](https://hackaday.com)
* [Build Your Own Smartphone-Connected Door Lock With a Raspberry Pi](https://lifehacker.com/build-your-own-smartphone-connected-door-lock-with-a-ra-1791424901) on [Lifehacker](https://lifehacker.com/)
