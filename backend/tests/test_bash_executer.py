"""Bash executer tests"""
import os
import unittest
import logging

from bash_executer import BashExecuter


prepare = [
    { "command": "node --version", "out": r"v20.\d+.\d+"},
    { "command": "npm install npm"},
    { "command": "npm install @angular/cli"},
    { "command": "ng version"}
]

create_project = [
    { "command": "mkdir {project_name}"},
    { "cwd": "{project_name}", "command": "ls -la"}
]

delete_project = [
    { "command": "rm -R -f {project_name}"}
]

class TestBashExecuter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        workspace = "tests/tmp/workspace/"
        os.makedirs(os.path.dirname(workspace), exist_ok=True)
        cls.bash = BashExecuter(workspace, { "project_name": "my_project" })

    def test_execute_node_version(self):
        _, out, err = self.bash.execute("node --version")
        self.assertRegex(out, r"v20.\d+.\d+")
        self.assertFalse(err)

    def test_execute_ng_version(self):
        _, out, err = self.bash.execute("ng version")
        self.assertRegex(out, r"Angular CLI: 17.\d+.\d+")
        self.assertFalse(err)


    def test_create_project(self):
        ret = self.bash.execute_seq(create_project)
        self.assertEqual(len(ret), 2)
        ret = self.bash.execute_seq(delete_project)
        self.assertEqual(len(ret), 1)
        


if __name__ == '__main__':
    unittest.main()
