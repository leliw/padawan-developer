"""Chat module"""
import json
import os
from typing import Optional
from pydantic import BaseModel

from bash_executer import BashExecuter

class ChatDataScript(BaseModel):
    """Chat data script"""
    cwd: Optional[str] = None
    command: str
    out: Optional[str] = None

class ChatData(BaseModel):
    """Chat data"""
    executer: str
    script: list[ChatDataScript]


class Chat:
    def __init__(self, workspace: str, data: dict[str, ChatData] = None):
        self.data = data or {}
        if not workspace.endswith("/"):
            workspace += "/"
        os.makedirs(workspace, exist_ok=True)
        self.bash = BashExecuter(workspace)

    def load(self, file_name: str):
        """Load chat data from JSON file"""
        with open(file_name, "tr", encoding="utf-8") as file:
            data = json.load(file)
            self.data = {}
            for d in data.items():
                script = [s for s in d[1]["script"]]
                self.data[d[0]] = ChatData(executer=d[1]["executer"], script=script)

    def get_answer(self, question):
        """Get answer for the question"""
        commands = self.data.get(question)
        if commands:
            if commands.executer == "bash":
                return self.bash_execute(commands.script)
        return "I don't understand you"
    
    def bash_execute(self, script):
        """Execute bash script"""
        ret = []
        for s in script:
            cmd, out, err = self.bash.execute(s.command, s.cwd)
            ret.append(f"{cmd}\n{out}{err}")
        return "\n".join(ret)

