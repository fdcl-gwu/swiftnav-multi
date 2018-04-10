from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH, \
    SBP_MSG_VEL_NED, SBP_MSG_GPS_TIME
from sbp.msg import SBP
from sbp.settings import SBP_MSG_SETTINGS_WRITE


import argparse


def enable_simulator_mode(port='/dev/ttyUSB0', baud=115200):
    '''
    Set simulator mode on on the Multi

    Args:
        port: serial port [[default='/dev/ttyUSB0']
        baud: baud rate [default=115200]

    Returns:
        None
    '''

    print('Reading from {} at {}'.format(port, baud))
    print('Setting the simulator mode on ...')

    with PySerialDriver(port, baud) as driver:
        sbp_msg = SBP(SBP_MSG_SETTINGS_WRITE)
        sbp_msg.payload = 'simulator\0enabled\0True\0'
        sbp_msg = sbp_msg.pack()
        driver.write(sbp_msg)


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
