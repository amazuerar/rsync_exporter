#!/bin/bash
rsync --daemon -v --config rsyncd_example.conf &
cron -f &
python3 main.py -p rsync.log
