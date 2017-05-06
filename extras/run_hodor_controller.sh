#! /bin/bash

controllerlogfile="/home/pi/log/run_hodor_controller_"`date +%Y%m%d_%H%M%S`"_$$.log"
slackerlogfile="/home/pi/log/run_hodor_slacker_"`date +%Y%m%d_%H%M%S`"_$$.log"
cd /home/pi/repos/hodor_picontroller
export PYTHONUNBUFFERED=1
touch ${controllerlogfile}
touch ${slackerlogfile}
python hodor_controller/watcher.py --root /home/pi >> ${controllerlogfile} 2>&1 &
python hodor_slackbot/hodor_slacker.py --root /home/pi >> ${slackerlogfile} 2>&1 &
exit 0
