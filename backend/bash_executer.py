"""Executes bash commands"""
import logging
import os
import re
import subprocess


class BashExecuter:
    """Executes bash commands"""
    def __init__(self, cwd: str = None, params: dict[str, str] = None) -> None:
        self.cwd = cwd if cwd else ""
        self.params = params if params else {}
        self._log = logging.getLogger(__name__)

    def execute(self, command: str, cwd: str = "") -> tuple[str, str]:
        """Executes single bash command"""
        abs_cwd = os.path.join(self.cwd, cwd.format_map(self.params))
        process = subprocess.Popen(['bash'],
                                   cwd = abs_cwd,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        out, err = process.communicate(command.format_map(self.params))
        if err:
            self._log.warning(err)
        return out, err
    
    def execute_seq(self, commands: list[dict]):
        """Executes a whole sequence of bash commands"""
        for cmd in commands:
            self._log.info("$ %s", cmd["command"])
            out, _ = self.execute(cmd["command"], cmd.get("cwd", ""))
            self._log.info(">>> %s", out)
            if "out" in cmd:
                match = re.match(cmd["out"], out)
                if match:
                    self._log.info("ok")


prepare = [
    { "command": "node --version", "out": r"v20.\d+.\d+"},
    { "command": "npm install npm"},
    { "command": "npm install @angular/cli"},
    { "command": "ng version"}
]

create_project = [
    { "command": "mkdir {project_name}"},
    { "cwd": "{project_name}", "command": "ng new frontend --routing"},
    { "cwd": "{project_name}/frontend", "command": "ng add @angular/material --skip-confirmation"},
    { "cwd": "{project_name}/frontend", "command": "ng generate @angular/material:navigation nav"},
    { "cwd": "{project_name}/frontend", "command": "ng generate @angular/material:dashboard home"},
]

delete_project = [
    { "command": "rm -R {project_name}"}
]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bash = BashExecuter("/home/mleliwa/src/", { "project_name": "my_project" })
    bash.execute_seq(prepare)
    bash.execute_seq(create_project)
    #bash.execute_seq(delete_project)

