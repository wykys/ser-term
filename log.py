import sys
from colors import colors

PROMPT = colors.fg.blue + colors.bold + '>>> ' + colors.reset

def err(s = ''):
    print( colors.fg.red + colors.bold + 'Error: ' + s + colors.reset, file=sys.stderr)

def war(s = ''):
    print( colors.fg.yellow + colors.bold + 'Warning: ' + s + colors.reset, file=sys.stderr)

def ok(s = ''):
    print( colors.fg.green + colors.bold + 'OK: ' + s + colors.reset, file=sys.stdout)

def stdo(s = ''):
    print( colors.fg.white + colors.bold + s + colors.reset, file=sys.stdout)

def rx(s = '', prompt=True):
    print( '\r' + colors.fg.orange + colors.bold + 'Rx: ' + colors.reset + colors.fg.orange + s + colors.reset, file=sys.stdout, end='')
    if prompt:
        print('\n' + PROMPT, file=sys.stdout, end='')

def tx(s = ''):
    print( colors.fg.green + colors.bold + 'Tx: ' + colors.reset + colors.fg.green + s + colors.reset, file=sys.stdout)
