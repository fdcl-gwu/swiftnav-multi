from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.client.loggers.json_logger import JSONLogger
from sbp.navigation import SBP_MSG_BASELINE_NED, MsgBaselineNED

import argparse


def read_piksi(port='/dev/ttyUSB0', baud=115200):
    '''
    Reads the output from SwiftNav Piksi, parses the messege and prints.abs

    Args:
        port: serial port [[default='/dev/ttyUSB0']
        baud: baud rate [default=115200]

    Returns:
        None
    '''

    # open a connection to Piksi
    with PySerialDriver(port, baud) as driver:
        with Handler(Framer(driver.read, None, verbose=True)) as source:
            try:
                for msg, metadata in source.filter(SBP_MSG_BASELINE_NED):
                    # print out the N, E, D coordinates of the baseline
                    print "%.4f,%.4f,%.4f" % (msg.n * 1e-3, msg.e * 1e-3,
                                              msg.d * 1e-3)
            except KeyboardInterrupt:
                pass


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

    read_piksi(args.port[0], args.baud[0])
