"""Chat module"""
import json
import logging
import os
import re
from typing import Optional
from pydantic import BaseModel

from bash_executer import BashExecuter

class ChatDataScript(BaseModel):
    """Chat data script"""
    cwd: Optional[str] = None
    command: str
    out_regex: Optional[str] = None

class ChatData(BaseModel):
    """Chat data"""
    question: str
    regex: str
    params: list[str]
    executer: str
    script: list[ChatDataScript]


class Chat:
    def __init__(self, workspace: str, data: dict[str, ChatData] = None):
        self.data = data or []
        if not workspace.endswith("/"):
            workspace += "/"
        os.makedirs(workspace, exist_ok=True)
        self.workspace = workspace
        self.bash = BashExecuter(workspace)
        self.params ={}
        self._log = logging.getLogger(__name__)

    def load(self, file_name: str):
        """Load chat data from JSON file"""
        with open(file_name, "tr", encoding="utf-8") as file:
            data = json.load(file)
            for d in data.items():
                question = d[0].strip().lower()
                regex, params = self._question2regex(question)
                executer = d[1]["executer"].strip().lower()
                script = [s for s in d[1]["script"]]
                self.data.append(ChatData(question=question, regex=regex, params=params, executer=executer, script=script))

    def _question2regex(self, question: str) -> tuple[str, list[str]]:
        """Convert question to regex"""
        regex = question.replace("{", "(?P<").replace("}", ">[^ ]+)")
        params = [p[1:-1] for p in re.findall(r"{[^}]+}", question)]
        return regex, params
    
    def get_answer(self, question: str) -> list[dict[str,str]]:
        """Get answer for the question"""
        q = question.strip().lower()
        if q == 'help':
            return self.get_help_answer()
        commands, params = self.get_commands(q)
        # merge new params with existing
        if params:
            self.params = self.params | params
        if commands:
            return self.execute_commands(commands)
        else:
            return [{"channel": "padawan", "text": "I don't understand you"}]

    def get_help_answer(self) -> list[dict[str,str]]:
        """Returns help message with available commands"""
        cmds = [cmd.question for cmd in self.data]
        return [{"channel": "padawan", "text": "You can use:\n" + "\n".join(cmds)}]

    def get_commands(self, question: str) -> Optional[tuple[ChatData, dict[str,str]]]:
        """Get commands for the question"""
        for cmd in self.data:
            match = re.search(cmd.regex, question)
            if match:
                params = match.groupdict()
                return (cmd, params)
        return None, None
    
    def execute_commands(self, commands: ChatData) -> list[dict[str,str]]:
        """Execute commands with proper executor"""
        if commands.executer == "bash":
            return self.bash_execute(commands.script)
        else:
            return [ {"channel": "padawan", "text": f"I can't handle {commands.executer}"}]

    def bash_execute(self, script) -> list[dict[str,str]]:
        """Execute bash script"""
        ret = []
        for s in script:
            cmd, out, err = self.bash.execute(s.command, cwd=s.cwd, params=self.params)
            ret.append({"channel": "bash_cmd", "text": f"$ {cmd}\n"})
            if out:
                if s.out_regex:
                    files = self.parse_out(out, s.out_regex)
                    if files:
                        ret.append({"channel": "files", "files": files})        
                ret.append({"channel": "bash_out", "text": out})
            if err:
                ret.append({"channel": "bash_err", "text": err})
        return ret

    def parse_out(self, out: str, out_reqex: Optional[str]) -> list[str]:
        """Parse output with regex
        
        if property name ends with "_full_path" it will be returned as file.
        """
        if out_reqex:
            match = re.search(out_reqex, out)
            if match:
                params = match.groupdict()
                self.params = self.params | params
                return [self.format_with_params("/{project_name}/" + v) for k, v in params.items() if k.endswith("_full_path")]
            
    def format_with_params(self, text: str) -> str:
        """Format text with params"""
        return text.format_map(self.params)
    
    def get_project_path(self) -> str:
        """Get project path"""
        return self.format_with_params(self.workspace + "{project_name}/")
                