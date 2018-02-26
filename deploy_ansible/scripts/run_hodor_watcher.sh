#! /bin/bash

controllerlogfile="{{ slackbot_log_dir }}/run_hodor_controller_"`date +%Y%m%d_%H%M%S`"_$$.log"

export PYTHONUNBUFFERED=1
touch ${controllerlogfile}
rm -f /var/run/hodor_controller.pid
cd {{ controller_run_dir }} && \
python {{ controller_install_dir }}/hodor_controller/watcher.py \
--root {{ controller_run_dir }} >> ${controllerlogfile} 2>&1
