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

*NOTE*: Description of the RFID reader and supporting hardware is TBD

For information on the Raspberry Pi software, including the `hodor_watcher`
program in `hodor_controller` and the `hodor_slacker` program in
`hodor_slackbot` please consult the
[Raspberry Pi Readme](docs/rpi_software/README.md) in the `docs/rpi_software`
directory.
