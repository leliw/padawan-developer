import unittest
import sys
import logging

from pydantic import BaseModel

project_path = '/'.join(__file__.split('/')[:-2])
sys.path.append(project_path)
logging.basicConfig(level=logging.DEBUG)

from storage.basic_storage import BasicStorage

class T(BaseModel):
    a: int
    b: int

class TestBasicStorage(unittest.TestCase):

    STORAGE_PATH = "tests/tmp"

    def test_basic_storage_string(self):
        storage = BasicStorage(self.STORAGE_PATH)
        storage.put('key', 'value')
        self.assertEqual(storage.get('key'), 'value')
        self.assertEqual(storage.get('key', file_ext='txt'), 'value')
        storage.delete('key')
        self.assertIsNone(storage.get('key'))

    def test_basic_storage_bin(self):
        storage = BasicStorage(self.STORAGE_PATH)
        storage.put('key', b'value')
        self.assertEqual(storage.get('key'), b'value')
        self.assertEqual(storage.get('key', file_ext="bin"), b'value')
        storage.delete('key')
        self.assertIsNone(storage.get('key'))

    def test_basic_storage_dict(self):
        storage = BasicStorage("test/tmp")
        storage.put('key', {"a": 1, "b": 2})
        self.assertEqual(storage.get('key'), {"a": 1, "b": 2})
        self.assertEqual(storage.get('key', file_ext="json"), {"a": 1, "b": 2})
        storage.delete('key')
        self.assertIsNone(storage.get('key'))

    def test_basic_storage_pydantic(self):
        storage = BasicStorage("test/tmp")
        t = T(a=1, b=2)
        storage.put('key', t)
        self.assertEqual(storage.get('key'), {"a": 1, "b": 2})
        self.assertEqual(storage.get('key', file_ext="json"), {"a": 1, "b": 2})
        self.assertEqual(storage.get('key', model_class=T), t)
        storage.delete('key')
        self.assertIsNone(storage.get('key'))

if __name__ == '__main__':
    unittest.main()