"""TypeSript tokenizer and parser"""
from __future__ import annotations
from typing import Any, Iterator
from tokenizer.basic_tokenizer import BasicTokenizer
from tokenizer._parser import ParseNode, BaseParser

# JavaScript and TypeScript keywords
js_keywords = ("break", "case","catch","class","const","continue","debugger",
               "default","delete","do","else","export","extends","false",
               "finally","for","function","if","import","in","instanceof",
               "new","null","return","super","switch","this","throw",
               "true","try","typeof","var","void","while","with","yield")
ts_keywords = js_keywords + \
            ("any","as","asserts","async","await","boolean","constructor",
              "declare","enum","from","get","implements","infer","interface",
              "is","keyof","let","module","namespace","never","readonly",
              "require","number","object","of","package","private","protected",
              "public","set","static","string","symbol","type","undefined",
              "unique","unknown","void")
ts_blocks =[
    ("[COMMAND]", None, "[SEMICOLON]"),
    ("[BRACED]", "[LBRACE]", "[RBRACE]"),
    ("[PARENT]", "[LPAREN]", "[RPAREN]")
]


class TypeScriptTokenizer(BasicTokenizer):
    """A simple regex-based tokenizer for TypeScript."""
    def __init__(self):
        super().__init__(keywords=ts_keywords)


class TypeScriptParser(BaseParser):
    """Parse TypeScript code"""
    def __init__(self):
        super().__init__(tokenizer = TypeScriptTokenizer(), blocks=ts_blocks)

    def parse_to_document(self, text: str) -> TypeScriptDocument:
        """Parse text to document object"""
        tree = self.parse(text)
        doc = TypeScriptDocument(self._tokenizer, self, tree)
        return doc


class TypeScriptDocument:
    """Parsed TypeScript document"""
    def __init__(self, tokenizer: BasicTokenizer, parser: BaseParser, parse_tree: ParseNode):
        self.tokenizer = tokenizer
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