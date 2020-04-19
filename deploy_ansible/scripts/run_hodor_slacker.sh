#! /bin/bash

slackerlogfile="{{ slacker_log_dir }}/run_hodor_slacker.log"

export PYTHONUNBUFFERED=1

cd {{ slacker_run_dir }} && \
python {{ slacker_install_dir }}/hodor_slackbot/hodor_slacker.py \
--root {{ slacker_run_dir }} >> ${slackerlogfile} 2>&1
