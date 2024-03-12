import unittest
import sys
import logging

from pydantic import BaseModel
from anytree import Node, RenderTree
from anytree.resolver import Resolver
from knowledge_base import KbTreeItem, KnowledgeBase

project_path = '/'.join(__file__.split('/')[:-2])
sys.path.append(project_path)
logging.basicConfig(level=logging.DEBUG)

from storage.basic_storage import BasicStorage


class TestKnowledgeBaseService(unittest.TestCase):

    STORAGE_PATH = "tests/tmp"

    def setUp(self):
        root = Node("<root>")
        self.kb = KnowledgeBase(root)
        s0 = Node("General", parent=root, isDir=True)
        Node("sub0B", parent=s0)
        Node("sub0A", parent=s0)
        s1 = Node("Angular", parent=root, isDir=True)
        Node("sub1A", parent=s1)
        Node("sub1B", parent=s1, bar=8)
        s1c = Node("sub1C", parent=s1)
        Node("sub1Ca", parent=s1c)
        print(RenderTree(self.kb.root_node))


    def test_get_items(self):
        items = self.kb.list_items("")
        self.assertCountEqual(items, [
            KbTreeItem.model_validate({"name": "General", "path": "/General", "isDir": True, "isLeaf": False}),
            KbTreeItem.model_validate({"name": "Angular", "path": "/Angular", "isDir": True, "isLeaf": False})
        ])

if __name__ == '__main__':
    unittest.main()