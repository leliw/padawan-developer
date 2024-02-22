"""Basic tokenizer"""
import re

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
    "EQUALS": '=',
    "COLON": ':',
    "SEMICOLON": ';',
    "COMMA": ',',
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

class Token:
    """A simple token representation."""

    PAD = "[PAD]"
    UNK = "[UNK]"
    MASK = "[MASK]"
    SPACE = '[WHITESPACE]'
    NL = '[NL]'
    IDENTIFIER = '[IDENTIFIER]'

    def __init__(self, token_type: str, value: str):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

basic_whitespace_tokens = [Token.SPACE, Token.NL]

class BasicTokenizer:
    """A simple regex-based tokenizer."""

    def __init__(self, special_characters = None, rules = None, keywords = None):
        """Create a new tokenizer with the given rules."""
        self.special_characters = special_characters if special_characters else basic_special_characters
        if rules is None:
            rules = basic_rules
        self.keywords = keywords
        self.rules = [(f"[{name}]", re.compile('\\'+c)) for name, c in self.special_characters.items()]
        self.rules += [(f"[{name}]", re.compile(pattern)) for name, pattern in rules]
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

    def tokenize(self, text: str) -> list[Token]:
        """Tokenize the given text."""
        tokens = []
        position = 0
        while position < len(text):
            match = None
            for name, pattern in self.rules:
                match = pattern.match(text, position)
                if match:
                    value = match.group(0)
                    tokens.append(Token(name, value))
                    position = match.end()  # Update position to the end of the match
                    break
            if not match:
                raise SyntaxError(f'Unexpected character: {text[position]}')
        if self.keywords:
            tokens = self._tokenize_keywords(tokens)
        return tokens

    def _tokenize_keywords(self, tokens: list[Token]) -> list[Token]:
        """Convert identifiers to uppercase if they are keywords."""
        ret = []
        for token in tokens:
            t = token.type
            v = token.value
            if t == Token.IDENTIFIER and v in self.keywords:
                ret.append(Token(f"[{v.upper()}]", v))
            else:
                ret.append(token)
        return ret

    def detokenize(self, tokens: list[Token]) -> str:
        """Convert the given tokens back to a string."""
        return ''.join([t.value for t in tokens])

    def print_tokens(self, tokens: list[Token]):
        print([(t.type, t.value) for t in tokens])

    def remove_wthitespaces(
            self, tokens: list[Token], whiespace_tokens: list[Token] = None
            ) -> dict[int, Token]:
        """Remove whitespace and newline tokens."""
        if whiespace_tokens is None:
            whiespace_tokens = basic_whitespace_tokens
        ret = {}
        for index, token in enumerate(tokens):
            if token.type not in whiespace_tokens:
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
        ret = (self.vocab.get(t, self.vocab[Token.UNK]), self.vocab.get(f"[{v}]", self.vocab[Token.UNK]))
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
