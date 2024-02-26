"""TypeScript parser tests"""
import unittest

from tokenizer.type_script import TypeScriptParser

CODE="""
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor() { }
}
"""

class TestTypeScriptParser(unittest.TestCase):
    """TypeScript parser tests"""
    def test_parse_and_unparse(self):
        """Converts code to parse tree and back to text"""
        t = TypeScriptParser()
        tree = t.parse(CODE)
        self.assertEqual(CODE, tree.unparse())

    def test_parse(self):
        """Converts code to parse tree"""
        t = TypeScriptParser()
        doc = t.parse_to_document(CODE)
        self.assertEqual(3, len(doc.children))
        self.assertEqual("[IMPORTS]", doc.children[0].type)
        self.assertEqual("[INTERFACES]", doc.children[1].type)
        self.assertEqual("[CLASSES]", doc.children[2].type)


if __name__ == '__main__':
    unittest.main()
