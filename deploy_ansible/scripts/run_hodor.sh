#! /bin/bash

controllerlogfile="{{ slackbot_log_dir }}/run_hodor_controller_"`date +%Y%m%d_%H%M%S`"_$$.log"
slackerlogfile="{{ slackbot_log_dir }}/run_hodor_slacker_"`date +%Y%m%d_%H%M%S`"_$$.log"
cd /home/pi/repos/hodor_picontroller
export PYTHONUNBUFFERED=1
touch ${controllerlogfile}
touch ${slackerlogfile}
( cd {{ controller_run_dir }} && python {{ controller_install_dir }}/hodor_controller/watcher.py --root {{ controller_run_dir }} >> ${controllerlogfile} 2>&1 & )
( cd {{ slackbot_run_dir }} && python {{ slackbot_install_dir }}/hodor_slackbot/hodor_slacker.py --root {{ slackbot_run_dir }} >> ${slackerlogfile} 2>&1 & )
exit 0
