#!/bin/bash

echo " "
echo "Setting rover GPS to simulator mode ..."
python2 write_from_ini_file.py -p /dev/ttyS0 -f settings_files/rover_simulator_mode.ini
echo " "
echo "Task finished."
