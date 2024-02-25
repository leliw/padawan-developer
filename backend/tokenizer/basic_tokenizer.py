"""Basic tokenizer"""
from typing import Iterator
from ._tokenizer import Token, BaseTokenizer, basic_special_characters, basic_rules, basic_whitespace_tokens


class BasicTokenizer(BaseTokenizer):
    """A simple regex-based tokenizer."""

    def __init__(self, special_characters = None, rules = None, keywords = None):
        """Create a new tokenizer with the given rules."""
        super().__init__()
        self.special_characters = special_characters or basic_special_characters
        if rules is None:
            rules = basic_rules
        self.keywords = keywords
        self.add_rule_characters([(name, c) for name, c in self.special_characters.items()])
        self.add_rule_patterns(rules)
        unique_rules = list(set([name for name, _ in self.rules]))
        # Special tokens
        self.vocab = {Token.PAD: 0, Token.UNK: 1, Token.MASK: 2}
        # Numeric tokens
        first = len(self.vocab)
        for i in range(0, 255):
            self.vocab[f"[{str(i)}]"] = first + i - 1
        # Rule tokens
        first = len(self.vocab)
        for i, rule in enumerate(unique_rules):
            self.vocab[rule] = first + i
        # Keyword tokens
        if keywords:
            first = len(self.vocab)
            for i, keyword in enumerate(keywords):
                self.vocab[f"[{keyword.upper()}]"] = first + i

        self.id_to_token = {id_: token for token, id_ in self.vocab.items()}
        self.temp_vocab = []

    def tokenize(self, text: str) -> Iterator[Token]:
        """Tokenize the given text."""
        tokens = super().tokenize(text)
        if self.keywords:
            tokens = self._tokenize_keywords(tokens)
        return tokens

    def _tokenize_keywords(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Convert identifiers to uppercase if they are keywords."""
        for token in tokens:
            t = token.type
            v = token.value
            if t == Token.IDENTIFIER and v in self.keywords:
                yield Token(f"[{v.upper()}]", v)
            else:
                yield token

    def print_tokens(self, tokens: list[Token]):
        print([(t.type, t.value) for t in tokens])

    def remove_whitespaces(
            self, tokens: list[Token], whitespace_tokens: list[Token] = None
            ) -> dict[int, Token]:
        """Remove whitespace and newline tokens."""
        if whitespace_tokens is None:
            whitespace_tokens = basic_whitespace_tokens
        ret = {}
        for index, token in enumerate(tokens):
            if token.type not in whitespace_tokens:
                ret[index] = token
        return ret

    def _convert_token_to_id(self, token):
        t = token.type
        if t in [Token.IDENTIFIER, '[STRING]', '[NUMBER]']:
            v = self.get_temp_vocab_index(token.value)
        elif t in [Token.SPACE, Token.NL]:
            v = len(token.value)
        else:
            v = None
        ret = (self.vocab.get(t, self.vocab[Token.UNK]),
                              self.vocab.get(f"[{v}]", self.vocab[Token.UNK]))
        return ret

    def get_temp_vocab_index(self, value: str):
        if value not in self.temp_vocab:
            self.temp_vocab.append(value)
        return self.temp_vocab.index(value)

    def _convert_id_to_token(self, token_id):
        t = self.id_to_token.get(token_id[0], Token.UNK)
        spec = t[1:-1]
        keyword = t[1:-1].lower()
        # t =  if t not in [Token.PAD, Token.UNK, Token.MASK] else t
        if spec in self.special_characters.keys():
            v = self.special_characters[spec]
        elif self.keywords and keyword in self.keywords:
            v = keyword
        elif t in [Token.IDENTIFIER, '[STRING]', '[NUMBER]']:
            i = self.id_to_token.get(token_id[1])
            v = self.temp_vocab[int(i[1:-1])]
        elif t in [Token.SPACE, Token.NL]:
            l = self.id_to_token.get(token_id[1])
            if l is not None:
                l = l[1:-1]
                if t == Token.NL:
                    v = '\n' * int(l)
                else:
                    v = ' ' * int(l)
            else:
                v = Token.UNK
        else:
            v = None
        return Token(t, v)
