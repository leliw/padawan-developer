from .._parser import BaseParser, ParseNode
from tokenizer.type_script.method import TypeScriptMethod
from .node import TypeScriptNode


from typing import Iterator


class TypeScriptClass(TypeScriptNode):
    """TypeScript class definition"""
    def __init__(self, parser: BaseParser, node: ParseNode) -> None:
        super().__init__(parser, node)
        gen = self._children_wws()
        for node in gen:
            if node.type == "[CLASS]":
                nn = next(gen)
                self.name = nn.value

    def find_methods(self) -> Iterator[TypeScriptMethod]:
        """Returns classes"""
        body = next(self.find_children("[BRACED]"))
        gen = body._children_wws()
        for node in gen:
            if node.type in ["[CONSTRUCTOR]", "[IDENTIFIER]"]:
                params = next(gen)
                yield TypeScriptMethod(self.parser, node, params)

    def add_method(self, sentence: str) -> None:
        """Adds new method to the class"""
        inserted = self.parser.parse("\n" + sentence)
        for node in self.node.children:
            if node.type == "[BRACED]":
                ins_index = len(node.children) - 2
                node.children[ins_index:ins_index] = [inserted]