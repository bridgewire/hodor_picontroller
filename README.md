# hodor_picontroller
Raspberry Pi-based door controller

## Overview of Contents

* `deploy_ansible` - Scripts to install Hodor onto a Raspberry Pi using Ansible
* `extras` - random utility scripts
* `hodor_controller` - Door controller program
* `hodor_slackbot` - Monitor program communicating door accesses to Slack
* `hodor_slackbot_configfiles` - example configuration files
* `setup.py` - installation script for `hodor_controller` and `hodor_slackbot`
* `unit_test_suite.py` - test script for `hodor_controller` and `hodor_slackbot`

*NOTE*: Description of the RFID reader and supporting hardware is TBD

## Overview of Program Operation

### hodor_controller Operation

On a Raspberry Pi the `hodor_controller` program monitors the Raspberry Pi serial port
for RFID card ID's scanned by an external receiver device and compares it against
a local file `bw_cardkey.csv`.  As card ID's are scanned, messages are written
to a log file and to an `events` directory to be read by `hodor_slackbot`.

The messages in the `events` directory are formatted as simple JSON files.
Each file contains a single JSON object with a single key named `message`,
the value of which is a text string to be posted to a Slack channel.

### hodor_slacker Operation

The `hodor_slackbot` program reads a configuration file (YAML-formatted,
normally in `/home/pi/.hodor_slacker_config.yml`) and watches the `events`
directory for messages.  As messages appear, they are read in sorting order
and posted to the slack channel per the configuration file.

## Developing and Testing off the Pi

One can work on the code locally off of a Raspberry Pi by running the scripts
in the local repository.

One can run the programs locally using:
```
    python hodor_controller/watcher.py

    python hodor_slackbox/hodor_slacker.py
```
To run the test suite, one can run:
```
    python unit_test_suite.py
```
Alternatively, one can install and test the codes using `setup.py`:
```
    python setup.py develop

    python setup.py test
```

## Deploying with Ansible

The [Ansible](http://www.ansible.com) playbook in the `deploy_ansible` directory can be used to install the programs onto a new Raspberry Pi.  The details of their integration and operation on the Pi are described in the following section.

To use the contents of the `deploy_ansible` directory, one should have Python installed with `pip` and `virtualenv`.  Running the deployment system will perform a project-local installation of Ansible to run the deployment.  

### Preparing for Playbook Use

As a prerequisite to using the playbook, one should prepare an OpenSSH key pair and install the public key on the target Raspberry Pi in `/home/pi/.ssh/authorized_keys`.

The next thing Ansible needs to perform a deployment is the name or address of the machine where the installation is to be performed.  To do this one should copy the example configuration to `inv.yml`, which is the inventory file name expected by the Makefile driving the deployment process:
```
    cp example_inventory.yml inv.yml
```
and edit the line that reads "`example.com:`" and replace `example.com` to match the name of the intended target machine.

### Running the Install

Once the aforementioned preparations are complete, one should be able to perform an installation simply by typing:
```
    make
```
The deployment process will prepare itself by creating a project-local subenvironment using `virtualenv`, install Ansible into it, then run the ansible playbook in `hodor_playbook.yml`.

## System Integration and Operation on the Pi

*NOTE*: some details will need updating after cookbook tweaks

Standard installation per the aforementioned Ansible playbook involves installing several files in several different places.

* SysV-style init scripts are installed in `/etc/init.d` (`hodor_watcher` and `hodor_slacker`) to integrate the programs into the Raspberry Pi's boot process
* Wrapper scripts (written for `bash`) invoked by the init scripts (`run_hodor_watcher.sh` and `run_hodor_slacker.sh`) run the main programs, set up log files and create PID files to track the process ID's of running programs.
* The program files proper as well as supporting files and directories are installed and configured to run out of the `/home/pi` directory.

An important proviso is that one important file is not installed by this process: the `.hodor_slacker_config.yml` file needed by `hodor_slackbot`.  This must be installed by hand in the `/home/pi` directory.  At this time, Ansible Vault, which is a feature to handle sensitive data, is not currently being used.
