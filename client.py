#!/usr/bin/env python3
# wykys
# client for ser-term configuration

import asyncio
import websockets
import port_protocol
import sys


async def client(uri, cmd):
    async with websockets.connect(uri) as websocket:
        await websocket.send(cmd)
        response = await websocket.recv()
        print(response)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('No command...')
        exit(-1)

    cmd = ''
    for word in sys.argv[1:]:
        cmd += word + ' '
    cmd = cmd.strip()

    asyncio.get_event_loop().run_until_complete(
        client(port_protocol.ProtocolConfig.URL, cmd)
    )
