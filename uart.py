#!/usr/bin/env python3
# wykys
# library for basic async UART manipulation


import asyncio
import serial_asyncio
from singleton import singleton


@singleton
class UART(object):
    def __init__(
                self,
                port='',
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                delay=0
            ):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.delay = delay
        """
        self.timeout = 0
        self.xonxoff = False
        self.rtscts = False
        self.dsrdtr = False
        """

        self.queue_rx = asyncio.Queue()
        self.queue_tx = asyncio.Queue()

        self.is_open = False
        self._is_conf = False

        self._reader = None
        self._writer = None
        self._task_recv = None
        self._task_send = None

    async def _send(self):
        try:
            while not self._is_conf:
                await asyncio.sleep(0.1)
            while True:
                msg = await self.queue_tx.get()
                if self.delay:
                    for char in msg:
                        self._writer.write(char.encode())
                        await asyncio.sleep(self.delay)
                else:
                    self._writer.write(msg.encode())
                self.queue_tx.task_done()
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            pass

    async def _recv(self):
        try:
            while not self._is_conf:
                await asyncio.sleep(0.1)
            msg = ''
            while True:
                symbol = await self._reader.read(n=1)
                symbol = symbol.decode()
                if symbol == '\r' or symbol == '\n':
                    if len(msg) > 0:
                        self.queue_rx.put_nowait(msg)
                        msg = ''
                else:
                    msg += symbol

        except asyncio.CancelledError:
            pass

    async def _conf(self):
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            url=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
        )
        self._is_conf = True

    def run(self):
        if not self.is_open:
            asyncio.ensure_future(self._conf())
            self._task_recv = asyncio.ensure_future(self._recv())
            self._task_send = asyncio.ensure_future(self._send())
            self.is_open = True

    def stop(self):
        self.is_open = False
        self._task_recv.cancel()
        self._task_send.cancel()


UART = UART()


################################################################################
# Testing
################################################################################
if __name__ == '__main__':
    UART.__init__('/dev/ttyUSB0', 38400)
    UART.queue_tx.put_nowait('AT\r\n')
    UART.run()
    UART.stop()
    loop = asyncio.get_event_loop()
    loop.run_forever()
