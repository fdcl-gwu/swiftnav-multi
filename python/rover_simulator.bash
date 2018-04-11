#!/bin/bash

echo "\nSetting rover GPS to simulator mode ...\n"
python2 write_from_ini_file.py -f settings_files/rover_simulator_mode.ini
echo "\nTask finished."
