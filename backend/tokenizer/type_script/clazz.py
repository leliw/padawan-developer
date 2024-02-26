from .._parser import BaseParser, ParseNode
from tokenizer.type_script.method import TypeScriptMethod
from .node import TypeScriptNode


from typing import Iterator


class TypeScriptClass(TypeScriptNode):
    """TypeScript class definition"""
    def __init__(self, parser: BaseParser, node: ParseNode) -> None:
        super().__init__(parser, node)
        self.name = self.get_child_after("[CLASS]").value

    def find_methods(self) -> Iterator[TypeScriptMethod]:
        """Returns classes"""
        body = next(self.find_children("[BRACED]"))
        gen = body._children_wws()
        for node in gen:
            if node.type in ["[CONSTRUCTOR]", "[IDENTIFIER]"]:
                params = next(gen)
                yield TypeScriptMethod(self.parser, node, params)

    def add_method(self, command: str) -> None:
        """Adds new method to the class"""
        inserted = self.parser.parse("\n" + command)
        for node in self.node.children:
            if node.type == "[BRACED]":
                ins_index = len(node.children) - 2
                node.children[ins_index:ins_index] = [inserted]
    
    def add(self, command: str) -> None:
        """Adds new propery or method to the class"""
        inserted = TypeScriptNode(self.parser, self.parser.parse("\n\n  " + command).children[0])
        print(inserted)
        it = self._get_command_type(inserted)
        block = self.get_child_after("[CLASS]", "[BRACED]")
        if it == "[PROPERTY]":
            i = 1
        else: 
            i = len(block.children) -2 
        block.children[i:i] = inserted.children

    def _get_command_type(self, node: TypeScriptNode) -> str:
        nt = node.get_child_after("[IDENTIFIER]").type
        return "[METHOD]" if nt == "[PARENT]" else "[PROPERTY]"
