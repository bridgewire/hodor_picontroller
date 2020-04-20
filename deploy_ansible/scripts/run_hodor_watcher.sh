#! /bin/bash

watcherlogfile="{{ watcher_log_dir }}/run_hodor_watcher.log"

export PYTHONUNBUFFERED=1

cd {{ watcher_run_dir }} && \
python3 {{ watcher_install_dir }}/hodor_controller/watcher.py \
--root {{ watcher_run_dir }} --dev /dev/ttyUSB0 >> ${watcherlogfile} 2>&1
