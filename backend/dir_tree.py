"""Read directory structure and list items in a directory"""
import os
from typing import List
from fastapi import HTTPException
from pydantic import BaseModel

class DirectoryNotFoundException(Exception):
    def __init__(self, path: str, message: str = None):
        message = message or f"Directory not found: {path}"
        self.message = message
        super().__init__(self.message)
        
class DirItem(BaseModel):
    """Directory item"""
    name: str
    path: str
    is_dir: bool
    has_items: bool

class DirTree:
    def __init__(self, cwd: str):
        self.cwd = cwd
        print(self.cwd)

    def list_subdirs(self, path: str) -> List[DirItem]:
        """List subdirectories in a directory"""
        return self.list_items(path, files_include=False)
    
    def list_items(self, path: str, files_include=True) -> List[DirItem]:
        """List items in a directory"""
        full_path, path = self._create_full_path(path)
        items = []
        for item in os.listdir(full_path):
            item_path = os.path.join("/", path, item)
            item_full_path = os.path.join(full_path, item)
            if os.path.isdir(item_full_path):
                subitems = files_include or [sub for sub in os.listdir(item_full_path) if os.path.isdir(os.path.join(item_full_path, sub))]
                items.append(DirItem(name=item, path=item_path, is_dir=True, has_items=bool(subitems)))
            elif files_include:
                items.append(DirItem(name=item, path=item_path, is_dir=False, has_items=False))
        return items

    def _create_full_path(self, path: str) -> tuple[str, str]:
        if path.startswith("/"):
            path = path[1:]
        full_path = os.path.join(self.cwd, path)
        if not os.path.exists(full_path):
            raise DirectoryNotFoundException(full_path)
        return full_path, path