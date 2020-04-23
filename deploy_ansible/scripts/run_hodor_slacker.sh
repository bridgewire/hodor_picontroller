#! /bin/bash

slackerlogfile="{{ slacker_run_dir }}/log/hodor_run_slacker.log"

export PYTHONUNBUFFERED=1

# call the script without requiring package installation to
# support editing and testing in situ
cd {{ slacker_run_dir }} && \
python3 {{ slacker_install_dir }}/hodor_slackbot/hodor_slacker.py \
--root {{ slacker_run_dir }} >> ${slackerlogfile} 2>&1
