#!/bin/bash

echo " "
echo "Setting rover GPS to default settings ..."
python2 write_from_ini_file.py -p /dev/ttyS0 -f settings_files/rover_moving_baseline.ini
echo " "
echo "Task finished."
