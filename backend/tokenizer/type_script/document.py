from typing import Iterator

from .._parser import BaseParser, ParseNode

from .node import TypeScriptNode
from .clazz import TypeScriptClass


class TypeScriptDocument(TypeScriptNode):
    """Parsed TypeScript document"""
    def __init__(self, parser: BaseParser, node: ParseNode):
        super().__init__(parser, node)

    def is_import(self, command: ParseNode) -> bool:
        """This is import command?"""
        return any(x.type=="[IMPORT]" for x in command.children)

    def is_class(self, command: ParseNode) -> bool:
        """This is class definition?"""
        return any(x.type=="[CLASS]" for x in command.children)

    def find_imports(self) -> Iterator[ParseNode]:
        """Returns import nodes"""
        for command in self.node.children:
            if self.is_import(command):
                yield command

    def add_import(self, sentence: str) -> None:
        """Adds import sentence (in import group)"""
        inserted = self.parser.parse("\n" + sentence)
        imports = False
        for index, command in enumerate(self.node.children):
            if not imports and self.is_import(command):
                imports = True  # Import block starts
            elif imports and not self.is_import(command):
                # Import block ended -> insert here
                self.node.children[index:index] = [inserted]
                return
        # No import block -> insert at beginning
        self.node.children = [inserted, *self.node.children]

    def find_classes(self) -> Iterator[TypeScriptClass]:
        """Returns classes"""
        for command in self.node.children:
            if self.is_class(command):
                yield TypeScriptClass(self.parser, command)
