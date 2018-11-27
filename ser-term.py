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
                MenuItem(text='[F2] Open port', handler=self.key_uart_open),
                MenuItem(text='[F3] Close port', handler=self.key_uart_close),
                MenuItem(
                    text='[F4] End line',
                    children=[
                        MenuItem('LF   \\n', handler=lambda: self.end_line_update('\n')),
                        MenuItem('CR   \\r', handler=lambda: self.end_line_update('\r')),
                        MenuItem('CRLF \\r\\n', handler=lambda: self.end_line_update('\r\n')),
                    ]
                ),
                MenuItem(text='[F10] Quit', handler=self.key_application_quit),
            ],
        )

        if args.end_line == 'LF':
            self.end_line = '\n'
        elif args.end_line == 'CR':
            self.end_line = '\r'
        else:
            self.end_line = '\r\n'
        self.end_line_update()

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
    def key_application_quit(self, event=None):
        get_app().exit()

    @key_bindings.add('f2')
    def key_uart_open(self, event=None):
        UART.run()

    @key_bindings.add('f3')
    def key_uart_close(self, event=None):
        UART.stop()

    @key_bindings.add('f4')
    def key_end_line(self, event=None):
        tui.end_line_update(shift=True)

    def cmd_line_accept_handler(self, handler):
        line = ''.join(('Tx: ', handler.text))
        console_append(self.console, line)
        UART.queue_tx.put_nowait(handler.text + self.end_line)

    def end_line_update(self, symbol=None, shift=None):
        if symbol:
            self.end_line = symbol

        if shift:
            if self.end_line == '\n':
                self.end_line = '\r'
                self.menu.menu_items[-2].text = '[F4] End line CR'
            elif self.end_line == '\r':
                self.end_line = '\r\n'
                self.menu.menu_items[-2].text = '[F4] End line CRLF'
            else:
                self.end_line = '\n'
                self.menu.menu_items[-2].text = '[F4] End line LF'

        if self.end_line == '\n':
            self.menu.menu_items[-2].text = '[F4] End line LF'
        elif self.end_line == '\r':
            self.menu.menu_items[-2].text = '[F4] End line CR'
        else:
            self.menu.menu_items[-2].text = '[F4] End line CRLF'

    def run(self):
        prompt_toolkit.eventloop.use_asyncio_event_loop()
        asyncio.get_event_loop().run_until_complete(
            self.app.run_async().to_asyncio_future()
        )


if __name__ == '__main__':
    UART.__init__(args.port, args.baudrate, delay=args.delay)
    UART.run()
    tui = TUI()
    server = PortServer(tui.console)
    asyncio.ensure_future(read(tui.console))
    server.run()
    tui.run()
