# wykys
# lexer for ser-term highlight

from pygments import token
from pygments.lexer import RegexLexer


class SerTermLexer(RegexLexer):
    name = 'SerTermLexer'
    aliases = ['SerTermLexer']
    filenames = ['*.SerTermLexer']

    tokens = {
        'root': [
            (r'^Rx:', token.Keyword),
            (r'^Tx:', token.Generic.Error),
            (r'^CMD:', token.Operator),
        ]
    }
