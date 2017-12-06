# wykys

import serial
import time
import os
import subprocess
import log

class uart:
    def __init__(self):
        """ initialization """
        self.name = 'CP2102'
        self.ser = serial.Serial()
        self.port = self.find_device()
        self.open_connection()

    def __del__(self):
        """ destructor """
        self.close_connection()

    def cmd_delay(self):
        """ command delay """
        time.sleep(0.02)

    def find_device(self):
        """ find port when is connected oscilloscope """
        dev_folder = '/dev/serial/by-id'
        dev = ''
        if os.path.exists(dev_folder):
            try:
                dev = subprocess.check_output('ls -l ' + dev_folder + ' | grep ' + self.name, shell=True).decode('utf-8').strip()
            except subprocess.CalledProcessError as e:
                pass

        if not (self.name in dev):
            log.err(self.name + ' is not connected')
            exit(1)

        port = '/dev/' + dev.split('../')[-1]
        log.ok(self.name + ' is connected to ' + port)

        return port

    def open_connection(self):
        """ open connection """
        self.ser.port = self.port
        self.ser.baudrate = 38400 # 115200
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.parity = serial.PARITY_NONE
        self.ser.bytesize = serial.EIGHTBITS

        self.ser.timeout = 0.1 # in seconds
        try:
            self.ser.open()
            log.ok('port {} is open'.format(self.port))
        except serial.SerialException:
            log.err('port {} opening is fail'.format(self.port))
            exit(1)

        time.sleep(2)
        self.ser.reset_input_buffer()

    def close_connection(self):
        """ end connection """
        self.ser.close()
        log.ok('port is close')

    def read_byte(self):
        """ read one byte """
        tmp = self.ser.read(1)
        if tmp == b'':
            return None
        return int.from_bytes(tmp, byteorder='little', signed=False)

    def send_byte(self, byte):
        """ write one byte """
        self.ser.write(bytes((byte,)))
        time.sleep(0.01)

    def write(self, cmd):
        """ send command """
        if type(cmd) == str:
            for c in cmd:
                self.send_byte(ord(c))
                self.cmd_delay()
            self.send_byte(ord('\r'))
