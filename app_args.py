# wykys
# arguments parser for ser-term

import argparse
from uart import BAUDRATE

parser = argparse.ArgumentParser('ser-term')

parser.add_argument(
    '-b',
    '--baudrate',
    dest='baudrate',
    action='store',
    type=int,
    default=115200,
    choices=BAUDRATE,
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

parser.add_argument(
    '-e',
    '--end-line',
    dest='end_line',
    action='store',
    type=str,
    default='LF',
    choices=[
        'LF', 'CR', 'CRLF'
    ],
    help='end line'
)

parser.add_argument(
    '-d',
    '--delay',
    dest='delay',
    action='store',
    type=float,
    default=0,
    help='time delay between symbols in seconds'
)

args = parser.parse_args()
