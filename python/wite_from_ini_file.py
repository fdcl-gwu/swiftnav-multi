from __future__ import print_function

from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.settings import SBP_MSG_SETTINGS_WRITE_RESP, MsgSettingsWrite, \
    MsgSettingsSave, MsgSettingsReadReq, SBP_MSG_SETTINGS_READ_RESP


import argparse
import configparser
import time


read_response_wait_dict = {}


def confirm_write(source, section, setting, value):
    '''
    Read the written values and check if it is set correctly

    Args:
        source: Handler object
        section: section of the settings
        settings: setting to be set
        value: set values

    Returns:
        status: bool - True of written settings are confirmed
    '''

    attempts = 0
    retries = 5
    while (attempts < retries):
        attempts += 1
        actual_value = read(source, section, setting)
        if value != actual_value:
            # value doesn't match, but could be a rounding issue
            try:
                float_val = float(actual_value)
                float_actual_val = float(value)
                if abs(float_val - float_actual_val) > 0.000001:
                    # value doesn't match, try again
                    continue
                else:
                    # value matches after allowing imprecision
                    return True
            except (TypeError, ValueError):
                continue
        else:
            # value matches
            return True


def write(source, section, setting, value):
    '''
    Writes the value of a given setting to the Multi.

    Args:
        source: Handler object
        section: section of the settings
        settings: setting to be set
        value: set values

    Returns:
        None
    '''

    write_retries = 5
    attempts = 0

    # print('Writing: section={}, setting={}, value={}'.format(section,
    #       setting, value))

    while (attempts < write_retries):
        attempts += 1

        reply = {'status': 0}

        def cb(msg, **metadata):
            reply['status'] = msg.status

        source.add_callback(cb, SBP_MSG_SETTINGS_WRITE_RESP)

        source(MsgSettingsWrite(setting='{}\0{}\0{}\0'.format(section, setting,
               value)))
        if confirm_write(source, section, setting, value):
            source.remove_callback(cb, SBP_MSG_SETTINGS_WRITE_RESP)
            break

    # print(reply['status'])


def read(source, section, setting):
    '''
    Read the value of a given setting from the Multi. Raise an error if a
    setting cannot be read

    Args:
        source: Handler object
        section: section of the settings
        settings: setting to be set

    Returns:
        None
    '''

    read_response_wait_dict[(section, setting)] = False
    attempts = 0
    response = False
    retries = 5
    while response is False and attempts < retries:
        # print("Attempting to read:section={}|setting={}".format(section,
        #       setting))
        source(MsgSettingsReadReq(setting='%s\0%s\0' % (section, setting)))
        time.sleep(0.5)
        response = read_response_wait_dict[(section, setting)]
        attempts += 1
    response = read_response_wait_dict[(section, setting)]
    if response is not False:
        # print("Successfully read setting \"{}\" in section \"{}\" with "
        #       "value \"{}\"".format(setting, section, response))
        return response
    else:  # never received read resp callback
        raise RuntimeError("Unable to read setting \"{}\" in section \"{}\" "
                           "after {} attempts. Setting may not exist.".format(
                           setting, section, retries))


def settings_callback(sbp_msg, **metadata):
    '''
    Calllback function for reading the settings
    '''
    section, setting, value, format_type = sbp_msg.payload.split(
        '\0')[:4]
    read_response_wait_dict[(section, setting)] = value


def write_ini_file(file_name, port='/dev/ttyUSB0', baud=115200):
    '''
    Write setting from an ini file to the Multi

    Args:
        file_name: file name of the ini file
        port: serial port [default='/dev/ttyUSB0']
        baud: baud rate [default=115200]

    Returns:
        None
    '''

    print('Reading from {} at {}'.format(port, baud))

    with PySerialDriver(port, baud) as driver:
        with Handler(Framer(driver.read, driver.write, verbose=True)) as source:

            parser = configparser.ConfigParser()
            parser.optionxform = str
            with open(file_name, 'r') as f:
                parser.read_file(f)

            source.add_callback(settings_callback, SBP_MSG_SETTINGS_READ_RESP)

            for section, settings in parser.items():
                print('\nSECTION: {}'.format(section))
                for setting, value in settings.items():
                    print('{} = {}'.format(setting, value))
                    write(source, section, setting, value)

            source(MsgSettingsSave())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            'Opens and reads the output of SwiftNav Piksi. \
             Developed based on Swift Navigation SBP example.'))
    parser.add_argument(
        '-f', '--file',
        default=['default.ini'],
        nargs=1,
        help='specify setting file to be written [default = \'default.ini\']')
    parser.add_argument(
        '-p', '--port',
        default=['/dev/ttyUSB0'],
        nargs=1,
        help='specify the serial port to use [default = \'/dev/ttyUSB0\']')
    parser.add_argument(
        '-b', '--baud',
        default=[115200],
        nargs=1,
        help='specify the baud rate [default = 115200]')
    args = parser.parse_args()

    print('Trying to write settings from {} to device at {}'.format(
          args.file[0], args.port[0]))
    write_ini_file(args.file[0], args.port[0], args.baud[0])
