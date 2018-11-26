#!/usr/bin/env python3
# wykys
# tui for ser-term

import asyncio

import prompt_toolkit
from prompt_toolkit import HTML, Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import (
    Box,
    Button,
    Frame,
    Label,
    MenuContainer,
    MenuItem,
    TextArea,
)

from lexer import SerTermLexer
from server import PortServer
from uart import UART
from app_args import args


def console_append(console, text):
    max_lines = 100
    console.text = ''.join((text, '\n', console.text))
    lines = console.text.split('\n')
    if len(lines) > max_lines:
        console.text = ''.join(line + '\n' for line in lines[:max_lines])


async def read(console):
    while True:
        rx = await UART.queue_rx.get()
        line = ''.join(('Rx: ', rx))
        console_append(console, line)
        UART.queue_rx.task_done()
        await asyncio.sleep(0.1)


class TUI(object):
    key_bindings = KeyBindings()

    def __init__(self):
        self.console = TextArea(
            scrollbar=True,
            focusable=False,
            line_numbers=False,
            lexer=PygmentsLexer(SerTermLexer),
        )

        self.cmd_line = TextArea(
            multiline=False,
            prompt=HTML('<orange>>>> </orange>'),
            style='bg: cyan',
            accept_handler=self.cmd_line_accept_handler,
            history=FileHistory('.ser-term-hist'),
            auto_suggest=AutoSuggestFromHistory(),
        )

        self.root = HSplit([
            self.console,
            self.cmd_line,
        ])

        self.menu = MenuContainer(
            self.root,
            menu_items=[
                MenuItem(text='[F2] open port', handler=self.uart_open),
                MenuItem(text='[F3] close port', handler=self.uart_close),
                MenuItem(text='[F10] quit', handler=self.application_quit),
            ]
        )

        self.layout = Layout(self.menu)
        self.layout.focus(self.root)

        self.key_bindings.add('s-tab')(focus_previous)
        self.key_bindings.add('tab')(focus_next)

        self.app = Application(
            layout=self.layout,
            key_bindings=self.key_bindings,
            full_screen=True,
            mouse_support=True,
        )

    @key_bindings.add('f10')
    @key_bindings.add('c-c')
    @key_bindings.add('c-d')
    @key_bindings.add('c-x')
    @key_bindings.add('c-q')
    @key_bindings.add('escape')
    def application_quit(self, event=None):
        get_app().exit()

    @key_bindings.add('f2')
    def uart_open(self, event=None):
        UART.run()

    @key_bindings.add('f3')
    def uart_close(self, event=None):
        UART.stop()

    def cmd_line_accept_handler(self, handler):
        line = ''.join(('Tx: ', handler.text))
        console_append(self.console, line)
        UART.queue_tx.put_nowait(handler.text + '\r\n')

    def run(self):
        prompt_toolkit.eventloop.use_asyncio_event_loop()
        asyncio.get_event_loop().run_until_complete(
            self.app.run_async().to_asyncio_future()
        )


if __name__ == '__main__':
    UART.__init__(args.port, args.baudrate)
    UART.run()
    tui = TUI()
    server = PortServer(tui.console)
    asyncio.ensure_future(read(tui.console))
    server.run()
    tui.run()
