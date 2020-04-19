#! /bin/bash

watcherlogfile="{{ slackbot_log_dir }}/run_hodor_watcher.log"

export PYTHONUNBUFFERED=1
# touch ${watcherlogfile}
# rm -f /var/run/hodor_controller.pid
cd {{ watcher_run_dir }} && \
python {{ watcher_install_dir }}/hodor_controller/watcher.py \
--root {{ watcher_run_dir }} >> ${watcherlogfile} 2>&1
