#! /bin/bash

slackerlogfile="{{ slacker_run_dir }}/log/run_hodor_slacker.log"

export PYTHONUNBUFFERED=1

cd {{ slacker_run_dir }} && \
python3 {{ slacker_install_dir }}/hodor_slackbot/hodor_slacker.py \
--root {{ slacker_run_dir }} >> ${slackerlogfile} 2>&1
