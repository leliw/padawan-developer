from typing import Iterator

from .._parser import BaseParser, ParseNode

from .node import TypeScriptNode
from .clazz import TypeScriptClass


class TypeScriptDocument(TypeScriptNode):
    """Parsed TypeScript document"""
    def __init__(self, parser: BaseParser, node: ParseNode):
        super().__init__(parser, node)

    def is_class(self, command: TypeScriptNode) -> bool:
        """This is class definition?"""
        return command.children_contains("[CLASS]")

    def find_imports(self) -> Iterator[ParseNode]:
        """Returns import nodes"""
        for command in self._children_wws():
            if command.children_contains("[IMPORT]"):
                yield command

    def add_import(self, sentence: str) -> None:
        """Adds import sentence (in import group)"""
        inserted = self.parser.parse("\n" + sentence)
        imports = False
        for index, command in enumerate(self.get_children()):
            if not imports and command.children_contains("[IMPORT]"):
                imports = True  # Import block starts
            elif imports and not command.children_contains("[IMPORT]"):
                # Import block ended -> insert here
                self.node.children[index:index] = [inserted]
                return
        # No import block -> insert at beginning
        self.node.children = [inserted, *self.node.children]

    def add_interface(self, sentence: str) -> None:
        """Adds import sentence (in import group)"""
        inserted = self.parser.parse("\n\n" + sentence)
        imports = False
        for index, command in enumerate(self.get_children()):
            if not imports and command.children_contains("[IMPORT]"):
                imports = True  # Import block starts
            elif imports and not command.children_contains("[IMPORT]"):
                # Import block ended -> insert here
                self.node.children[index:index] = inserted.children
                return
        # No import block -> insert at beginning
        self.node.children = [inserted, *self.node.children]

    def find_classes(self) -> Iterator[TypeScriptClass]:
        """Returns classes"""
        for command in self.get_children():
            if self.is_class(command):
                yield TypeScriptClass(self.parser, command)
