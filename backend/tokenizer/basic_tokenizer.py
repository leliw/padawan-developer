import re


basic_rules = {
    "NUMBER": r'\d+',
    "PLUS": r'\+',
    "MINUS": r'-',
    "TIMES": r'\*',
    "DIVIDE": r'/',
    "LPAREN": r'\(',
    "RPAREN": r'\)',
    "LBRACE": r'\{',
    "RBRACE": r'\}',
    "LBRACKET": r'\[',
    "RBRACKET": r'\]',
    "IDENTIFIER": r'[a-zA-Z_][a-zA-Z0-9_]*',
    "EQUALS": r'=',
    "COLON": r':',
    "SEMICOLON": r';',
    "COMMA": r',',
    "STRING": r'"(\\.|[^"\\])*"',
    "NL": r'\n',
    "WHITESPACE": r'\s+'
}

class Token:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class BasicTokenizer:
    def __init__(self, rules):
        self.rules = [(name, re.compile(pattern)) for name, pattern in rules.items()]

    def tokenize(self, text: str) -> list[Token]:
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
                print(position, text[position:])
                raise SyntaxError(f'Unexpected character: {text[position]}')
        return tokens
    
    def print_tokens(self, tokens: list[Token]):
        print([(t.type, t.value) for t in tokens])

    def remove_wthitespaces(self, tokens: list[Token]):
        ret = []
        for token in tokens:
            if token.type not in ['WHITESPACE', 'NL']:
                ret.append(token)
        return ret
