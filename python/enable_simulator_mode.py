from __future__ import print_function

from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.msg import SBP
from sbp.settings import SBP_MSG_SETTINGS_WRITE, SBP_MSG_SETTINGS_SAVE, \
    SBP_MSG_SETTINGS_WRITE_RESP, MsgSettingsWrite, MsgSettingsSave


import argparse
import time


def enable_simulator_mode(port='/dev/ttyUSB0', baud=115200):
    '''
    Set simulator mode to ON on the Multi

    Args:
        port: serial port [[default='/dev/ttyUSB0']
        baud: baud rate [default=115200]

    Returns:
        None
    '''

    print('Reading from {} at {}'.format(port, baud))
    print('Setting the simulator mode on ...')

    with PySerialDriver(port, baud) as driver:
        with Handler(Framer(driver.read, driver.write, verbose=True)) as source:

            reply = {'status': 0}

            def cb(msg, **metadata):
                reply['status'] = msg.status

            source.add_callback(cb, SBP_MSG_SETTINGS_WRITE_RESP)
            print("Added status callback ...")
            sbp_msg = SBP(SBP_MSG_SETTINGS_WRITE)
            sbp_msg.payload = 'simulator\0enabled\0True\0'
            sbp_msg = sbp_msg.pack()
            driver.write(sbp_msg)

            time.sleep(2)
            # source(MsgSettingsWrite(setting='%s\0%s\0%s\0' % ('simulator', 'enabled', 'True')))
            print(reply['status'])
            # sbp_save = SBP(SBP_MSG_SETTINGS_SAVE)
            # sbp_save = sbp_save.pack()
            # driver.write(sbp_save)
            source(MsgSettingsSave())
            print(reply['status'])

            source.remove_callback(cb, SBP_MSG_SETTINGS_WRITE_RESP)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            'Opens and reads the output of SwiftNav Piksi. \
            Developed based on Swift Navigation SBP example.'))
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

    enable_simulator_mode(args.port[0], args.baud[0])
