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
        tree = t.parse(CODE)
        print(tree)
        self.assertEqual(2, len(tree.children))
        self.assertEqual("[COMMAND]", tree.children[0].type)
        self.assertEqual("[COMMAND]", tree.children[1].type)


if __name__ == '__main__':
    unittest.main()
