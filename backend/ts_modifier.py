"""Modifies TypeScript files"""
import logging
import os

from tokenizer.type_script import TypeScriptParser, TypeScriptDocument, TypeScriptClass, TypeScriptMethod


class TypeScriptModifier:
    """Modifies TypeScript files
    
    Parameters
    ----------
    cwd: str
        Current Working Directory - parent path for all files
    params: dict[str, str]
        Set of parameters used while file modification
    """
    def __init__(self, cwd: str = None, params: dict[str, str] = None) -> None:
        self.cwd = cwd if cwd else ""
        self.params = params if params else {}
        self.parser = TypeScriptParser()
        self.doc: TypeScriptDocument = None
        self._log = logging.getLogger(__name__)

    def open_file(self, file: str) -> None:
        """Opens file for modification"""
        file_path = os.path.join(self.cwd, file.format_map(self.params))
        self.doc = self.parser.parse_file_to_document(file_path)

    def add(self, ts_command: str) -> None:
        """Adds first level command into TypeScript document (import, interface, ...)"""
        self.doc.add_command(ts_command)

    def add_in_class(self, class_name: str, ts_command: str) -> None:
        """Adds property or method inside given class"""
        clazz = self._get_class(class_name)
        clazz.add(ts_command)

    def add_parameter_in_method(self, class_method_name: str, ts_command: str) -> None:
        """Adds property or method inside given class"""
        class_name, method_name = class_method_name.split(".")
        clazz = self._get_class(class_name)
        method = self._get_method(clazz, method_name)
        method.add_parameter(ts_command)

    def _get_class(self, class_name: str) -> TypeScriptClass:
        for c in self.doc.find_classes():
            if c.name == class_name:
                return c
        return None
    
    def _get_method(self, clazz: TypeScriptClass, method_name: str) -> TypeScriptMethod:
        for m in clazz.find_methods():
            if m.name == method_name:
                return m
        return None
    