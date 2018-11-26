# ser-term
Serial terminal for debugging.

This application strives to facilitate the development of `UART`-enabled electronics. The main advantage of this terminal is that it allows to share the port and configure it using the command line. Use this one in `Makefile` projects, if the circuit has only one `UART` and you use the `bootloader`, you can arrange to release the port for the duration of the program recording and then return it again.

The terminal is based on `prompt_toolkit`, `asyncio_serial` and `websocket` libraries.
