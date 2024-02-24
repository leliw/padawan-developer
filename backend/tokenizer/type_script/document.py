from tokenizer._parser import BaseParser, ParseNode
from tokenizer.basic_tokenizer import BasicTokenizer
from .clazz import TypeScriptClass


from typing import Iterator


class TypeScriptDocument:
    """Parsed TypeScript document"""
    def __init__(self, parser: BaseParser, parse_tree: ParseNode):
        self.parser = parser
        self.tree = parse_tree

    def unparse(self) -> str:
        """Returns document text"""
        return self.tree.unparse()

    def is_import(self, command: ParseNode) -> bool:
        """This is import command?"""
        return any(x.type=="[IMPORT]" for x in command.children)

    def is_class(self, command: ParseNode) -> bool:
        """This is class definition?"""
        return any(x.type=="[CLASS]" for x in command.children)

    def find_imports(self) -> Iterator[ParseNode]:
        """Returns import nodes"""
        for command in self.tree.children:
            if self.is_import(command):
                yield command

    def add_import(self, sentence: str) -> None:
        """Adds import sentence (in import group)"""
        inserted = self.parser.parse("\n" + sentence)
        imports = False
        for index, command in enumerate(self.tree.children):
            if not imports and self.is_import(command):
                imports = True  # Import block starts
            elif imports and not self.is_import(command):
                # Import block ended -> insert here
                self.tree.children[index:index] = [inserted]
                return
        # No import block -> insert at beginning
        self.tree.children = [inserted, *self.tree.children]

    def find_classes(self) -> Iterator[TypeScriptClass]:
        """Returns classes"""
        for command in self.tree.children:
            if self.is_class(command):
                yield TypeScriptClass(self.parser, command)