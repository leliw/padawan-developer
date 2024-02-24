from .._parser import BaseParser, ParseNode
from .node import TypeScriptNode


class TypeScriptMethod(TypeScriptNode):
    """TypeScript method"""
    def __init__(self, parser: BaseParser, node: ParseNode, params: ParseNode) -> None:
        super().__init__(parser, node)
        self.name = node
        self.params = params

    def add_parameter(self, sentence: str) -> None:
        """Adds new method to the class"""
        ins_index = len(self.params.children) - 1
        sentence = ", " + sentence if ins_index > 2 else sentence
        inserted = self.parser.parse(sentence)
        self.params.children[ins_index:ins_index] = inserted.children