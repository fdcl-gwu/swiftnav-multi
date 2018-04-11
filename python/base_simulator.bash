#!/bin/bash

echo "\nSetting base GPS to simulator mode ...\n"
python2 write_from_ini_file.py -f settings_files/base_simulator_mode.ini
echo "\nTask finished."
