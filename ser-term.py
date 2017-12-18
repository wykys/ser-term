#!/usr/bin/python3
# wykys 2017

import log
import argparse
import threading
from uart import uart

def read(event):
    log.stdo('reading thread run')
    tmp = ''
    raw = []
    while True:
        buf = ser.read_byte()
        if type(buf) is int:
            if buf != ord('\n') and buf != ord('\r'):
                tmp += chr(buf)
                raw.append(buf)
            elif len(raw) > 0:
                log.rx(tmp)
                tmp = ''
                raw = []
        else:
            if tmp != '' and tmp != '\n' and tmp != '\r' and len(raw) > 0:
                log.rx(tmp)
                tmp = ''
                raw = []

        if kill_event.isSet():
            exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('ser-term')
    parser.add_argument('-n', '--name', dest='name', action='store', default='CP2102', help='device name')
    parser.add_argument('-b', '--baud', dest='baud', action='store', type=int, default=115200, choices=[50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200], help='baud rate')
    args = parser.parse_args()

    kill_event = threading.Event()
    kill_event.clear()

    ser = uart(name=args.name, baudrate=args.baud)

    thread = threading.Thread(target=read, args=(kill_event,))
    thread.start()

    while True:
        txt = input(log.PROMPT)
        if txt == 'exit':
            log.stdo(log.colors.fg.red + 'exit')
            kill_event.set()
            break
        elif txt[0] == ':':
            cmd = txt[1::]
            if cmd == 'info':
                print('baudrate: ', ser.ser.baudrate)
                print('bits: ', ser.ser.bytesize)
                print('parity: ', ser.ser._parity)
                print('stopbits: ', ser.ser.stopbits)
            elif 'set bd' in cmd:
                ser.ser.baudrate = int(cmd.split('set bd ')[1])
        elif txt != '':
            ser.write(txt)
            log.tx(txt)
