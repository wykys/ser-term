# wykys
# arguments parser for ser-term

import argparse

parser = argparse.ArgumentParser('ser-term')

parser.add_argument(
    '-b',
    '--baudrate',
    dest='baudrate',
    action='store',
    type=int,
    default=115200,
    choices=[
        50,
        75,
        110,
        134,
        150,
        200,
        300,
        600,
        1200,
        1800,
        2400,
        4800,
        9600,
        19200,
        38400,
        57600,
        115200,
    ],
    help='baud rate'
)

parser.add_argument(
    '-P',
    '--port',
    dest='port',
    action='store',
    default='/dev/ttyUSB0',
    help='device port'
)

args = parser.parse_args()
