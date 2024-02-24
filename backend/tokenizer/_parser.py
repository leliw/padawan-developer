"""Base code (any programic language) parser"""
from __future__ import annotations
from abc import ABC

from tokenizer._tokenizer import BaseTokenizer


class ParseNode:
    """Node of parsed tree"""
    def __init__(self, node_type, value, children: list[ParseNode] =None):
        self.type = node_type
        self.value = value
        self.children = children or []

    def add_child(self, child):
        """Adds child to node"""
        self.children.append(child)

    def __str__(self, level=0):
        ret = "  " * level + f"{self.type}: {self.value}\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def unparse(self) -> str:
        """Returns (oryginal) text"""
        if self.children:
            return ''.join([c.unparse() for c in self.children])
        else:
            return self.value


class BaseParser(ABC):
    """Base code (any programic language) parser"""
    def __init__(self, tokenizer: BaseTokenizer, blocks: list[tuple[str,str,str]]) -> None:
        super().__init__()
        self._tokenizer = tokenizer
        self.blocks = blocks
        self.block_starts = {block[1]:block for block in self.blocks}
        self.tokens = []

    def parse(self, content: str) -> ParseNode:
        """Parse given content"""
        self.tokens = self._tokenizer.tokenize(content)
        root = ParseNode("[ROOT]", "", self._parse_block())
        # root.add_child(self._parse_block(0))
        return root

    def _parse_block(self, end_block_token = None) -> list[ParseNode]:
        nodes = []
        while True:
            token = next(self.tokens, None)
            if not token:
                break
            node = ParseNode(token.type, token.value)
            if token.type in self.block_starts.keys():
                # Block starts
                block = self.block_starts.get(token.type)
                children = self._parse_block(block[2])
                nodes.append(ParseNode(block[0], "block", [node, *children]))
            elif end_block_token and token.type == end_block_token:
                # Block ends
                return [*nodes, node]
            elif not end_block_token:
                # Start command
                block = self.block_starts.get(None)
                children = self._parse_block(block[2])
                nodes.append(ParseNode(block[0], "", [node, *children]))
            else:
                nodes.append(node)
        return nodes
