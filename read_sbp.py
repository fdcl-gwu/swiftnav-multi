from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH, \
    SBP_MSG_VEL_NED

import argparse
import pdb


def read_rtk(port='/dev/ttyUSB0', baud=115200):
    '''
    Reads the RTK output from SwiftNav Piksi, parses the messege and prints.
    Piksi's must be configured to give RTK message through the serial port.
    NOTE: Current official sbp drivers only support python-2

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
                msg_list = [SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH,
                            SBP_MSG_VEL_NED]
                for msg, metadata in source.filter(msg_list):
                    print(msg.msg_type)
                    # pdb.set_trace()

                    # print "%.4f,%.4f,%.4f" % (msg.n * 1e-3, msg.e * 1e-3,
                    #                           msg.d * 1e-3)

            except KeyboardInterrupt:
                pass

    return


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

    read_rtk(args.port[0], args.baud[0])
