from __future__ import annotations
from typing import Any, Iterator

from .._parser import BaseParser
from .._parser import ParseNode


class TypeScriptNode:
    """ParseNode decorator for TypeScript"""
    def __init__(self, parser: BaseParser, node: ParseNode) -> None:
        self.parser = parser
        self.node = node

    def unparse(self) -> str:
        """Returns (oryginal) text"""
        return self.node.unparse()

    def find_children(self, type: str) -> Iterator[TypeScriptNode]: 
        """Returns children of given type"""
        for x in self._children_wws():
            if x.node.type == type:
                yield TypeScriptNode(self.parser, x)

    def _children_wws(self) -> Iterator[TypeScriptNode]:
        for x in self.node.children:
            if x.type not in ['[NL]', '[WHITESPACE]']:
                yield TypeScriptNode(self.parser, x)

    def __getattr__(self, __name: str) -> Any:
        return self.node.__getattribute__(__name)