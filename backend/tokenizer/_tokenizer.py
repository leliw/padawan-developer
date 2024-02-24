"""Base tokenizer"""
import re

from abc import ABC
from typing import Iterator

class Token:
    """A simple token representation."""
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
