
from pydantic import BaseModel, Field
from anytree import Node, Resolver

from storage import DirectoryStorage


class KbTreeItem(BaseModel):
    name: str
    path: str
    is_dir: bool = Field(..., alias="isDir")
    is_leaf: bool = Field(..., alias="isLeaf")

class KnowledgeBase:

    def __init__(self, root_node: Node):
        self.root_node = root_node
        self.resolver = Resolver('name')

    def get_node(self, path: str) -> Node:
        return self.resolver.get(self.root_node, path)
    
    def add_node(self, path: str, name: str, **kwargs):
        parent = self.get_node(path)
        Node(name, parent = parent, kwargs=kwargs)

    def add_directory(self, path: str, name: str):
        self.add_node(path, name, is_dir=True)

    def add_file(self, path: str, name: str):
        self.add_node(path, name, is_dir=False)

    def list_items(self, path: str, include_leaves = True) -> list[KbTreeItem]:
        ret = []
        for c in self.resolver.get(self.root_node, path).children:
            if include_leaves or not c.is_leaf:
                path = "/" + "/".join([str(node.name) for node in c.path if not node.is_root])
                is_dir = c.isDir if hasattr(c, "isDir") else False
                ret.append(KbTreeItem(name=c.name, path=path, isDir=is_dir, isLeaf=c.is_leaf))
        return sorted(ret, key=lambda x: x.name)
    
class KnowledgeBaseService:

    def __init__(self, base_path: str):
        self.storage = DirectoryStorage(base_path)

    def list_items(self, path: str) -> list[KbTreeItem]:
        return self.storage.list_items(path)

    def add_directory(self, path: str, name: str):
        self.kb.add_directory(path, name)

    def add_file(self, path: str, name: str):
        self.kb.add_file(path, name)

    def get_node(self, path: str) -> Node:
        return self.kb.get_node(path)