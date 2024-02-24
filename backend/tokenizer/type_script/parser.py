
from .._parser import BaseParser
from .document import TypeScriptDocument
from .tokenizer import TypeScriptTokenizer


ts_blocks =[
    ("[COMMAND]", None, "[SEMICOLON]"),
    ("[BRACED]", "[LBRACE]", "[RBRACE]"),
    ("[PARENT]", "[LPAREN]", "[RPAREN]")
]


class TypeScriptParser(BaseParser):
    """Parse TypeScript code"""
    def __init__(self):
        super().__init__(tokenizer = TypeScriptTokenizer(), blocks=ts_blocks)

    def parse_to_document(self, text: str) -> TypeScriptDocument:
        """Parse text to document object"""
        tree = self.parse(text)
        doc = TypeScriptDocument(self, tree)
        return doc
