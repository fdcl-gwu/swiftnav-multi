#!/bin/bash

echo "\nSetting rover GPS to default settings ...\n"
python2 write_from_ini_file.py -f settings_files/rover_default.ini
echo "\nTask finished."
