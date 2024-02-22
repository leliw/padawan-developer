"""Basic sentencizer"""
from tokenizer.basic_tokenizer import Token

class Sentence:

    def __init__(self, sentence_type: str, start: int, end: int, tokens: list[Token] = None ):
        self.type = sentence_type
        self.start = start
        self.end = end
        self.tokens = tokens

    def get_body(self) -> str:
        if self.tokens:
            return "".join([t.value for t in self.tokens[self.start:self.end]])
        return None

    def __str__(self):
        if self.tokens:
            return f'Sentence({self.type}, ({self.start}, {self.end}, "{self.get_body()}"))'
        return f'Sentence({self.type}, ({self.start}, {self.end}))'

basic_blocks =[
    ("BRACED", "[LBRACE]", "[RBRACE]")
]

class BasicSentencizer:

    def __init__(self, blocks: list[tuple[str,str,str]] = None, separator='[COMMA]'):
        self.blocks = blocks if blocks else basic_blocks
        self.separator = separator

        self.block_starts = {block[1]:block for block in self.blocks}

    def sentencize(self, tokens: list[Token]) -> list[Sentence]:
        sentences: list[Sentence] = []
        start = 0
        block_level = 0
        block = ()
        last = Sentence(None, 0,0)
        for index, token in enumerate(tokens):
            if token.type in self.block_starts.keys():
                if block_level == 0:
                    start = index + 1
                    block = self.block_starts.get(token.type)
                block_level += 1
            elif block and token.type == block[2]:
                block_level -= 1
                if block_level == 0:
                    last = Sentence(block[0], start, index, tokens)
                    sentences.append(last)
                    start = index + 1
                    block = ()
            elif token.type == self.separator and block_level == 0:
                last = Sentence("SENTENCE", start if start else last.end, index, tokens)
                sentences.append(last)
                start = index + 1
        if last.end < len(tokens)-1:
            last = Sentence("SENTENCE", last.end, len(tokens), tokens)
            sentences.append(last)
        return sentences
