#! /bin/bash

slackerlogfile="{{ slackbot_log_dir }}/run_hodor_slacker_"`date +%Y%m%d_%H%M%S`"_$$.log"

export PYTHONUNBUFFERED=1
touch ${slackerlogfile}
rm -f /var/run/hodor_slacker.pid
cd {{ slackbot_run_dir }} && \
python {{ slackbot_install_dir }}/hodor_slackbot/hodor_slacker.py \
--root {{ slackbot_run_dir }} >> ${slackerlogfile} 2>&1
