# wykys

import serial
from serial.tools import list_ports

import time
import os
import log

class uart:
    def __init__(self, name='CP2102', baudrate=115200, bytesize=8, parity='N', port=None):
        """ initialization """
        self.name = name
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.timeout = 0.1                 # in seconds
        if port == None:
            self.ser.port = self.find_device()
        else:
            self.ser.port = port
        self.open_connection()

    def __del__(self):
        """ destructor """
        self.close_connection()

    def cmd_delay(self):
        """ command delay """
        time.sleep(0.02)

    def find_device(self):
        """ find port when is connected device """
        for port in list_ports.comports():
            if port.description == self.name:
                return port.device

        log.err(self.name + ' is not connected')
        self.list_ports()
        exit(1)

    def list_ports(self):
        """ print list all ports """
        log.stdo('List all connected devices:')
        for port in list_ports.comports():
            print('    ', port.device, '\t', port.description)

    def open_connection(self):
        """ open connection """
        try:
            self.ser.open()
            log.ok('port {} is open'.format(self.ser.port))
        except serial.SerialException:
            log.err('port {} opening is fail'.format(self.ser.port))
            exit(1)

        time.sleep(2)
        self.ser.reset_input_buffer()

    def close_connection(self):
        """ end connection """
        self.ser.close()
        log.ok('port is close')

    def read_byte(self):
        """ read one byte """
        try:
            tmp = self.ser.read(1)
        except serial.SerialException:
            log.err('the device was disconnected')
            os.system('killall ser-term')

        if tmp == b'':
            return None
        return int.from_bytes(tmp, byteorder='little', signed=False)

    def send_byte(self, byte):
        """ write one byte """
        try:
            self.ser.write(bytes((byte,)))
        except serial.SerialException:
            log.err('the device was disconnected')
            os.system('killall ser-term')

        time.sleep(0.01)

    def write(self, cmd):
        """ send command """
        if type(cmd) == str:
            for c in cmd:
                self.send_byte(ord(c))
                self.cmd_delay()
            self.send_byte(ord('\r'))
