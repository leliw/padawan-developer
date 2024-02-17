import re


basic_rules = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('EQUALS', r'='),
    ('COLON', r':'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('STRING', r'"(\\.|[^"\\])*"'),
    ('NL', r'\n'),
    ('WHITESPACE', r'\s+'),
]

class Token:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class Tokenizer:
    def __init__(self, rules):
        self.rules = [(name, re.compile(pattern)) for name, pattern in rules]

    def tokenize(self, code):
        tokens = []
        position = 0
        while position < len(code):
            match = None
            for name, pattern in self.rules:
                match = pattern.match(code, position)
                if match:
                    value = match.group(0)
                    tokens.append(Token(name, value))
                    position = match.end()  # Zaktualizuj pozycję do końca dopasowanego fragmentu
                    break
            if not match:
                print(position, code[position:])
                raise SyntaxError(f'Unexpected character: {code[position]}')
            # Można dodać tutaj logikę do obsługi białych znaków lub komentarzy, jeśli potrzebne
        return tokens
    
    def print_tokens(self, tokens):
        print([(t.type, t.value) for t in tokens])

    def remove_wthitespaces(self, tokens):
        ret = []
        for token in tokens:
            if token.type not in ['WHITESPACE', 'NL']:
                ret.append(token)
        return ret
    
    def tokens_to_sentences(self, tokens: list) -> list:
        sentences = []
        start = None
        last = (0,0)
        for index, token in enumerate(tokens):
            if token.type == 'LBRACE' and start is None:
                start = index+1
            elif token.type == 'RBRACE' and start is not None:
                last = (start, index)
                start = None
                sentences.append(last)
            elif token.type == 'COMMA' and start is None:
                last = (last[1], index+1)
                sentences.append(last)
        if last[1] < len(tokens)-1:
            last = (last[1], len(tokens))
            sentences.append(last)
        ret = []
        for s in sentences:
            if tokens[s[1]-1].type == 'COMMA':
                ret.append((s[0], s[1]-1))
            else:
                ret.append((s[0], s[1]))
        return ret

