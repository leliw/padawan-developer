"""
Simple file based storage (key: value)
where key is a file name and value is a file content.
The key can contain any number "/" to create a tree of directories.
"""
import logging
import os
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


from .basic_storage import BasicStorage

class DirectoryItem(BaseModel):
    """Directory item"""
    name: str
    path: str
    is_dir: bool = Field(..., alias="isDir")
    is_leaf: bool = Field(..., alias="isLeaf")
    has_children: bool = Field(..., alias="hasChildren")

class DirectoryStorage(BasicStorage):
    """Stores data on disk in directories (tree)"""
    def __init__(self, base_path="data"):
        super().__init__(base_path)
        self._log = logging.getLogger(__name__)

    def list_items(self, sub_path: str, files_include=True) -> List[DirectoryItem]:
        """List items in a directory"""
        sub_path = sub_path.removeprefix("/") if sub_path else None
        full_path = Path(os.path.join(self._base_path, sub_path) if sub_path else self._base_path)
        items = []
        for item in os.listdir(full_path):
            item_path = os.path.join("/", sub_path, item)
            item_full_path = os.path.join(full_path, item)
            if os.path.isdir(item_full_path):
                subitems = [sub for sub in os.listdir(item_full_path) if os.path.isdir(os.path.join(item_full_path, sub))]
                items.append(DirectoryItem(name=item, path=item_path, isDir=True, isLeaf=not bool(subitems), hasChildren=bool(subitems)))
            elif files_include:
                items.append(DirectoryItem(name=item, path=item_path, isDir=False, isLeaf=True, hasChildren=False))
        return sorted(items, key=lambda x: (not x.is_dir, x.name))

    def get_directory_tree(self, sub_path: str = None, include_files = False) -> list:
        """Returns tree of directories in storage"""
        sub_path = sub_path.removeprefix("/") if sub_path else None
        full_path = Path(os.path.join(self._base_path, sub_path) if sub_path else self._base_path)
        if include_files or full_path.is_dir():
            children = [self._get_directory_children(e) for e in full_path.iterdir()]
            if children:
                return children
        return []
    
    def _get_directory_children(self, sub_path: str = None) -> dict|None:
        sub_path = Path(sub_path)
        if sub_path.is_dir():
            children = [self._get_directory_children(e) for e in sub_path.iterdir()]
            ret = {"name": sub_path.name}
            if children:
                ret["children"] = children
            return ret
        else:
            return None

    def _evaluate_sub_path_and_file_name(self, key: str) -> tuple[str, str]:
        """Returns sub_path and file_name from key where sub_path is a part of key before last '/' and file_name is a part after last '/'"""
        sub_paths = key.split("/", maxsplit=2)
        file_name = self._evaluate_file_name(sub_paths.pop())
        sub_path = os.path.join(*sub_paths) if sub_paths else None
        return (sub_path, file_name)