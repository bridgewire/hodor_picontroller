#! /bin/bash

watcherlogfile="{{ watcher_log_dir }}/run_hodor_watcher.log"

export PYTHONUNBUFFERED=1
# touch ${watcherlogfile}
# rm -f /var/run/hodor_controller.pid
cd {{ watcher_run_dir }} && \
python {{ watcher_install_dir }}/hodor_controller/watcher.py \
--root {{ watcher_run_dir }} --dev /dev/ttyUSB0 >> ${watcherlogfile} 2>&1
