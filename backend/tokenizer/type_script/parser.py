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

    def parse_file_to_document(self, file_path: str) -> TypeScriptDocument:
        """Parse file content to document object"""
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        tree = self.parse(file_content)
        doc = TypeScriptDocument(self, tree)
        return doc
