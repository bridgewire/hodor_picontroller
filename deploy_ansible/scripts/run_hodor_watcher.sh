#! /bin/bash

watcherlogfile="{{ watcher_run_dir }}/log/hodor_run_watcher.log"

export PYTHONUNBUFFERED=1

# call the script without requiring package installation to
# support editing and testing in situ
cd {{ watcher_run_dir }} && \
python3 {{ watcher_install_dir }}/hodor_controller/watcher.py \
--root {{ watcher_run_dir }} --dev /dev/ttyUSB0 >> ${watcherlogfile} 2>&1
