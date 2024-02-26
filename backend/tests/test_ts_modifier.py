"""Basic sententizer tests"""
import os
import unittest
import logging

from ts_modifier import TypeScriptModifier

logging.basicConfig(level=logging.DEBUG)


CODE = """
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor() { }
}
"""

class TestTypeScriptModifier(unittest.TestCase):
    """Tests TypeScriptModifier class"""
    @classmethod
    def setUpClass(cls) -> None:
        full_path = "tests/tmp/src/app/proxy/proxy.service.ts"
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as plik:
            plik.write(CODE)

    def test_open_file(self):
        """Tests open_file and parsing content"""
        t = TypeScriptModifier("tests/tmp")
        t.open_file("src/app/proxy/proxy.service.ts")
        self.assertEqual(3, len(list(t.doc.node.children)))     # Two sentences (import and class)

    def test_add_import(self):
        """Tests adding import command"""
        t = TypeScriptModifier("tests/tmp")
        t.open_file("src/app/proxy/proxy.service.ts")

        t.add("import { HttpClient } from '@angular/common/http';")

        expected = """
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor() { }
}
"""
        self.assertEqual(expected, t.doc.unparse())


    def test_add_in_class_property(self):
        """ Test adding property in class"""
        t = TypeScriptModifier("tests/tmp")
        t.open_file("src/app/proxy/proxy.service.ts")

        t.add_in_class("ProxyService", "private apiUrl = \"/api/proxy\";")

        expected = """
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  private apiUrl = "/api/proxy";

  constructor() { }
}
"""
        self.assertEqual(expected, t.doc.unparse())


    def test_add_in_class_method(self):
        """ Test adding method in class"""
        t = TypeScriptModifier("tests/tmp")
        t.open_file("src/app/proxy/proxy.service.ts")

        t.add_in_class("ProxyService", "private apiUrl = \"/api/proxy\";")
        t.add_in_class("ProxyService", """getStatus(): Observable<Status> {
        return this.http.get<Status>(this.apiUrl + '/status');
  }""")
        
        expected = """
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  private apiUrl = "/api/proxy";

  constructor() { }

  getStatus(): Observable<Status> {
        return this.http.get<Status>(this.apiUrl + '/status');
  }
}
"""
        self.assertEqual(expected, t.doc.unparse())


    def test_add_parameter_in_method(self):
        """Tests adding import command"""
        t = TypeScriptModifier("tests/tmp")
        t.open_file("src/app/proxy/proxy.service.ts")

        t.add("import { HttpClient } from '@angular/common/http';")
        t.add_parameter_in_method("ProxyService.constructor", "private http: HttpClient")

        expected = """
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ProxyService {

  constructor(private http: HttpClient) { }
}
"""
        self.assertEqual(expected, t.doc.unparse())





if __name__ == '__main__':
    unittest.main()
