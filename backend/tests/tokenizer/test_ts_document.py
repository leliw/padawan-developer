"""Testing TypeScript document manipulation"""
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

class TestTypeScriptDocument(unittest.TestCase):
    """Testing TypeScript document manipulation"""
    def test_find_imports(self):
        """Finds import commands"""
        p = TypeScriptParser()
        doc = p.parse_to_document(CODE)

        imports = list(doc.find_imports())

        self.assertEqual(1, len(imports))
        self.assertEqual("\nimport { Injectable } from '@angular/core';", imports[0].unparse())


    def test_add_import(self):
        """Adds import command"""
        p = TypeScriptParser()
        doc = p.parse_to_document(CODE)

        doc.add_import("import { HttpClient } from '@angular/common/http';")

        expected="""
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor() { }
}
"""
        self.assertEqual(expected, doc.unparse())


    def test_find_classes(self):
        """Finds classes"""
        p = TypeScriptParser()
        doc = p.parse_to_document(CODE)

        classes = list(doc.find_classes())

        self.assertEqual(1, len(classes))
        expected="""

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor() { }
}
"""
        self.assertEqual(expected, classes[0].unparse())
        self.assertEqual("ProxyService", classes[0].name)


    def test_add_method(self):
        """Adds class method"""
        p = TypeScriptParser()
        doc = p.parse_to_document(CODE)
        clazz = next(doc.find_classes())

        clazz.add_method("""
  getStatus(): Observable<Status> {
        return this.http.get<Status>(this.apiUrl + '/status');
  }""")
        expected="""
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor() { }

  getStatus(): Observable<Status> {
        return this.http.get<Status>(this.apiUrl + '/status');
  }
}
"""
        self.assertEqual(expected, doc.unparse())


    def test_find_method(self):
        """Finds class methods"""
        p = TypeScriptParser()
        doc = p.parse_to_document(CODE)
        clazz = next(doc.find_classes())

        methods = list(clazz.find_methods())
        self.assertEqual(1, len(methods))
        self.assertEqual("constructor", methods[0].name)


if __name__ == '__main__':
    unittest.main()
