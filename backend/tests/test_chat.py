import os
import unittest
import logging

from chat import Chat

CHAT_DATA = """
{"Create project xxx": {
    "executer": "bash",
    "script": [
        {"command": "mkdir xxx", "out": ""},
        {"command": "ls -la", "cwd": "xxx", "out": ""},
        {"command": "rmdir xxx", "out": ""}
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
        self.assertEqual(3, len(self.chat.data.get("create project xxx").script))


    def test_bash_commands(self):
        self.chat.load(TMP_FILE)

        resp = self.chat.get_answer("Create project xxx")[0]["text"]
        self.assertTrue(resp.startswith("$ mkdir xxx\n"))

if __name__ == '__main__':
    unittest.main()
