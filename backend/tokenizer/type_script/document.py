from typing import Iterator

from .._parser import BaseParser, ParseNode

from .node import TypeScriptNode
from .clazz import TypeScriptClass


class TypeScriptDocument(TypeScriptNode):
    """Parsed TypeScript document
    
    Parameters
    ----------
    parser: BaseParser
        Parser object used for parsing document
    node: ParseNode
        Root node of document
    file_path: str
        Parsed file path
    """
    sections = {
        "[IMPORTS]": "[IMPORT]", 
        "[INTERFACES]": "[INTERFACE]", 
        "[CLASSES]": "[CLASS]"
        }

    def __init__(self, parser: BaseParser, node: ParseNode, file_path: str = None):
        # Create empty sections
        node_sec = ParseNode(node.type, node.value)
        for sec, _ in TypeScriptDocument.sections.items():
            node_sec.add_child(ParseNode(sec))
        super().__init__(parser, node_sec)
        self.file_path = file_path
        # Fill secrtions with commands
        for command in node.children:
            section = self._command_section(TypeScriptNode(self.parser, command))
            self.add_command_in_section(command, section)

    def __str__(self) -> str:
        # Improves readability
        return self.node.__str__(skip_types=[
            "[NL]", "[WHITESPACE]", 
            "[LBRACE]", "[RBRACE]",
            "[LPAREN]", "[RPAREN]",
            ])

    def _command_section(self, command: TypeScriptNode) -> str:
        for section, token_type in TypeScriptDocument.sections.items():
            if command.children_contains(token_type):
                return section
        return None

    def add_command_in_section(self, command: ParseNode, section: str) -> None:
        """Adds command in specified section"""
        for sec in self.node.children:
            if sec.type == section:
                if command.children[0].type != '[NL]':
                    if len(sec.children) == 0:
                        command.children[0:0] = self.parser.parse("\n\n").children
                    else:
                        command.children[0:0] = self.parser.parse("\n").children
                sec.add_child(command)
                return
        self.node.add_child(command)    # Added at the end if not added earlier

    def get_section(self, section: str) -> Iterator[ParseNode]:
        """Returns nodes from section"""
        for sec in self.node.children:
            if sec.type == section:
                for command in sec.children:
                    yield command

    def find_imports(self) -> Iterator[ParseNode]:
        """Returns import nodes"""
        for node in self.get_section("[IMPORTS]"):
            yield node

    def add_command(self, command: str) -> None:
        """Adds first level command in proper section"""
        c = self.parser.parse(command)
        inserted = TypeScriptNode(self.parser, c.children[0])
        section = self._command_section(inserted)
        self.add_command_in_section(inserted, section)

    def find_classes(self) -> Iterator[TypeScriptClass]:
        """Returns classes"""
        for node in self.get_section("[CLASSES]"):
            yield TypeScriptClass(self.parser, node)
