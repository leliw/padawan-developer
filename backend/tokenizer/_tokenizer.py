"""Base tokenizer - base class for tokenizers

"""
import re
from abc import ABC
from typing import Iterator

basic_special_characters = {
    "PLUS": '+',
    "MINUS": '-',
    "TIMES": '*',
    "DIVIDE": '/',
    "LPAREN": '(',
    "RPAREN": ')',
    "LBRACE": '{',
    "RBRACE": '}',
    "LBRACKET": '[',
    "RBRACKET": ']',
    "LT" : '<',
    "GT" : '>',
    "EQUALS": '=',
    "COLON": ':',
    "SEMICOLON": ';',
    "COMMA": ',',
    "DOT": '.',
    "AT": "@"
}

basic_rules = [
    ("NUMBER", r'\d+'),
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("STRING", r'"(\\.|[^"\\])*"'),
    ('STRING', r"'(\\.|[^'\\])*'"),
    ("NL", r'\n+'),
    ("WHITESPACE", r'\s+')
]

basic_whitespace_tokens = ["[WHITESPACE]", "[NL]"]

class Token:
    """A token returned by Tokenizer
    
    Parameter
    ---------
    token_type : str
        Token type (coresponds wtih rule definition)
    value : str
        Real string content of token
    """
    def __init__(self, token_type: str, value: str):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    PAD = "[PAD]"
    UNK = "[UNK]"
    MASK = "[MASK]"
    SPACE = '[WHITESPACE]'
    NL = '[NL]'
    IDENTIFIER = '[IDENTIFIER]'


class BaseTokenizer(ABC):
    """A simple regex-based tokenizer."""
    def __init__(self) -> None:
        super().__init__()
        self.rules = []

    def add_rule_patterns(self, named_patterns: list[tuple[str, str]]) -> None:
        """Adds regex patterns as rules"""
        self.rules += [(f"[{name}]", re.compile(pattern)) for name, pattern in named_patterns]

    def add_rule_characters(self, named_characters: list[tuple[str, str]]) -> None:
        """Adds characters (like "=", "+", ...) as rules"""
        self.rules = [(f"[{name}]", re.compile('\\'+c)) for name, c in named_characters]

    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize the given text."""
        position = 0
        while position < len(text):
            match = None
            for name, pattern in self.rules:
                match = pattern.match(text, position)
                if match:
                    value = match.group(0)
                    yield Token(name, value)
                    position = match.end()  # Update position to the end of the match
                    break
            if not match:
                raise SyntaxError(f'Unexpected character: {text[position]}')

    def detokenize(self, tokens: Iterator[Token]) -> str:
        """Convert the given tokens back to a string."""
        return ''.join([t.value for t in tokens])
