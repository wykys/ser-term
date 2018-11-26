# wykys
# protocol for ser-term configuration


class ProtocolConfig(object):
    ADDRESS = 'localhost'
    PORT = '8765'
    URL = 'ws://{}:{}'.format(ADDRESS, PORT)


class PortState(object):
    OPEN = 'open'
    CLOSE = 'close'
    SHARE = 'share'


class PortInfo(object):
    GET_PORT = 'get port'
    GET_PORT_STATE = 'get port state'


class PortCommand(object):
    CMD_OPEN_PORT = 'cmd open port'
    CMD_CLOSE_PORT = 'cmd close port'
    CMD_SHARE_PORT = 'cmd share port'
    CMD_RETURN_PORT = 'cmd return port'
