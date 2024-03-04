import os
import unittest
import logging

from chat import Chat

CHAT_DATA = """
{"Create project {project_name}": {
    "executer": "bash",
    "script": [
        {"command": "mkdir {project_name}", "out": ""},
        {"command": "ls -la", "cwd": "{project_name}", "out": ""},
        {"command": "rmdir {project_name}", "out": ""}
        ]
    }
}
"""
TMP_FILE = "tests/tmp/chat_data.json"
WORKSPACE = "tests/tmp/workspace/"
class TestChat(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.chat = Chat(WORKSPACE)
        with open(TMP_FILE, "w") as file:
            file.write(CHAT_DATA)

    def test_do_not_understand(self):
        self.assertEqual(self.chat.get_answer("Sprechen sie deutsch?")[0]["text"], "I don't understand you")


    def test_load(self):
        self.chat.load(TMP_FILE)

        self.assertEqual(1, len(self.chat.data))
        cmd, _ = self.chat.get_commands("create project xxx")
        self.assertEqual(3, len(cmd.script))


    def test_bash_commands(self):
        self.chat.load(TMP_FILE)

        resp = self.chat.get_answer("Create project xyz")[0]["text"]
        self.assertTrue(resp.startswith("$ mkdir xyz\n"))

if __name__ == '__main__':
    unittest.main()
