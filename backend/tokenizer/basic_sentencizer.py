"""Basic sentencizer"""
from typing import Iterator
from tokenizer.basic_tokenizer import Token

class Sentence:

    def __init__(self, sentence_type: str, start: int, end: int, tokens: list[Token] = None ):
        self.type = sentence_type
        self.start = start
        self.end = end
        self.tokens = tokens

    def get_tokens(self) -> Iterator[str]:
        """Returns tokens within senstance"""
        if self.tokens:
            for token in self.tokens[self.start:self.end]:
                yield token

    def get_tokens_wws(self, ws_tokens = (Token.SPACE, Token.NL)) -> Iterator[str]:
        """Returns tokens within senstance without whitespaces"""
        if self.tokens:
            for token in self.tokens[self.start:self.end]:
                if token.type not in ws_tokens:
                    yield token

    def get_body(self) -> str:
        """Returns senstence text"""
        return "".join([t.value for t in self.get_tokens()])

    def __str__(self):
        if self.tokens:
            return f'Sentence({self.type}, ({self.start}, {self.end}, "{self.get_body()}"))'
        return f'Sentence({self.type}, ({self.start}, {self.end}))'

basic_blocks =[
    ("BRACED", "[LBRACE]", "[RBRACE]")
]

basic_whitespace_tokens = (Token.SPACE, Token.NL)

class BasicSentencizer:
    """Splits list of tokens into sentences"""
    def __init__(self, blocks: list[tuple[str,str,str]] = None, separator='[COMMA]'):
        self.blocks = blocks if blocks else basic_blocks
        self.separator = separator

        self.block_starts = {block[1]:block for block in self.blocks}

    def sentencize(self, tokens: list[Token]) -> list[Sentence]:
        """Splits list of tokens into sentences"""
        sentences: list[Sentence] = []
        start = 0
        block_level = 0
        block = ()
        sent = False
        last = Sentence(None, 0,0)
        for index, token in enumerate(tokens):
            if not block:
                # Not yet any block is opened
                if token.type in self.block_starts.keys():
                    # Block starts
                    if block_level == 0:
                        # It's first level block - will be returned
                        if not sent:
                            start = index + 1
                        block = self.block_starts.get(token.type)
                    block_level += 1
                elif token.type == self.separator:
                    # Sentence ended
                    last = Sentence("SENT", start, index, tokens)
                    sentences.append(last)
                    start = index + 1
                elif token.type not in basic_whitespace_tokens:
                    # Sentence started
                    sent = True
            else:
                # Block is opened
                if token.type == block[1]:
                    # Nested block started
                    block_level += 1
                elif token.type == block[2]:
                    # Block ends
                    block_level -= 1
                    if block_level == 0:
                        # It's first level block
                        if not sent:
                            last = Sentence(block[0], start, index, tokens)
                            sentences.append(last)
                            start = index + 1
                        block = ()

        if start < len(tokens)-1:
            last = Sentence("SENTENCE", start, len(tokens), tokens)
            sentences.append(last)
        return sentences
