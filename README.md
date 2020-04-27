# hodor_picontroller
Raspberry Pi-based door controller

## Overview of Contents

* `deploy_ansible` - Scripts to install Hodor onto a Raspberry Pi using Ansible
* `docs` - documentation
* `extras` - random utility scripts
* `hodor_controller` - Door controller program
* `hodor_slackbot` - Monitor program communicating door accesses to Slack
* `hodor_slackbot_configfiles` - example configuration files
* `setup.py` - installation script for `hodor_controller` and `hodor_slackbot`
* `unit_test_suite.py` - test script for `hodor_controller` and `hodor_slackbot`


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
