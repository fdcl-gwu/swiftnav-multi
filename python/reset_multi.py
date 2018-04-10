from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.piksi import SBP_MSG_RESET
from sbp.msg import SBP

import argparse


def reset(port='/dev/ttyUSB0', baud=115200):
    '''
    Resets the Multi.

    Args:
        port: serial port [[default='/dev/ttyUSB0']
        baud: baud rate [default=115200]

    Returns:
        None
    '''

    print('Reading from {} at {}'.format(port, baud))

    verify = raw_input('Are you sure want to reset the Multi? Y/[n]: ') or 'n'
    if verify == 'Y':
        print('Retting the Multi ...')
        with PySerialDriver(port, baud) as driver:
            reset_sbp = SBP(SBP_MSG_RESET)
            reset_sbp.payload = ''
            reset_sbp = reset_sbp.pack()
            driver.write(reset_sbp)
        print('Resetted the Multi.')
    else:
        print('Skipped resetting.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=('Resets the SwiftNav Piksi.'))
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

    reset(args.port[0], args.baud[0])
