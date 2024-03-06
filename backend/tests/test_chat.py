import os
import unittest
import logging

from chat import Chat

CHAT_DATA = """
{
    "Create project {project_name}": {
    "executer": "bash",
    "script": [
        {"command": "mkdir {project_name}", "out": ""},
        {"command": "ls -la", "cwd": "{project_name}", "out": ""},
        {"command": "rmdir {project_name}", "out": ""}
        ]
    },
    "Create service {service_name}": {
        "executer": "bash",
        "script": [
            {
                "command": "echo \\"CREATE src/app/services/proxy.service.spec.ts (352 bytes)\\nCREATE src/app/services/proxy.service.ts (134 bytes)\\"",
                "out_regex": "CREATE (?P<service_full_path>[a-z/_0-9]+.service.ts)"
            }
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

        self.assertEqual(2, len(self.chat.data))
        cmd, _ = self.chat.get_commands("create project xxx")
        self.assertEqual(3, len(cmd.script))


    def test_bash_commands(self):
        self.chat.load(TMP_FILE)

        resp = self.chat.get_answer("Create project xyz")[0]["text"]
        self.assertTrue(resp.startswith("$ mkdir xyz\n"))


    def test_get_answer(self):
        self.chat.load(TMP_FILE)

        resp = self.chat.get_answer("Create service users")
        
        self.assertEqual(3, len(resp))
        self.assertEqual("files", resp[1]["channel"])
        self.assertEqual("src/app/services/proxy.service.ts", resp[1]["files"][0])
        self.assertEqual("src/app/services/proxy.service.ts", self.chat.params["service_full_path"])


if __name__ == '__main__':
    unittest.main()
