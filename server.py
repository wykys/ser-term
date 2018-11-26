#!/usr/bin/env python3
# wykys
# server for ser-term configuration

import asyncio
import websockets
import port_protocol
from uart import UART
from uuid import uuid1


class PortServer(object):
    def __init__(self, console):
        self.console = console
        self.is_share = False
        self.uuid = None

    async def port_manager(self, websocket, path):
        async for message in websocket:
            response = self.analyze_message(message)
            await websocket.send(response)

    def run(self):
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(
                self.port_manager,
                port_protocol.ProtocolConfig.ADDRESS,
                port_protocol.ProtocolConfig.PORT
            )
        )

    def analyze_message(self, message):
        self.console.text = ''.join(('CMD: ', message, '\n', self.console.text))
        # GET ==================================================================
        if message == port_protocol.PortInfo.GET_PORT:
            return UART.port
        elif message == port_protocol.PortInfo.GET_PORT_STATE:
            if self.is_share:
                return port_protocol.PortState.SHARE
            elif UART.is_open:
                return port_protocol.PortState.OPEN
            else:
                return port_protocol.PortState.CLOSE

        # CMD ==================================================================
        elif message == port_protocol.PortCommand.CMD_OPEN_PORT:
            if not self.is_share:
                UART.run()
                return 'OPEN'
            else:
                return 'PORT IS OCCUPIED'
        ########################################################################
        elif message == port_protocol.PortCommand.CMD_CLOSE_PORT:
            if not self.is_share:
                UART.stop()
                return 'STOP'
            else:
                return 'PORT IS OCCUPIED'
        ########################################################################
        elif message == port_protocol.PortCommand.CMD_SHARE_PORT:
            if not self.is_share:
                self.is_share = True
                self.uuid = str(uuid1())
                UART.stop()
                return self.uuid
            else:
                return 'PORT IS OCCUPIED'
        ########################################################################
        elif port_protocol.PortCommand.CMD_RETURN_PORT in message:
            if self.is_share:
                uuid_key = message.split()[-1]
                if uuid_key == self.uuid:
                    self.is_share = False
                    UART.run()
                    return 'RETURN'
                else:
                    return 'ERROR'
            else:
                return 'ERROR'
        # ERR ==================================================================
        else:
            return 'ERROR'


################################################################################
# Testing
################################################################################
if __name__ == '__main__':
    server = PortServer()
    server.run()
    asyncio.get_event_loop().run_forever()
