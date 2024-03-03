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

    def execute(self, command: str, cwd: str = "") -> tuple[str, str, str]:
        """Executes single bash command
        
        Parameters
        ----------
        command : str
            bash command
        cwd : str
            working directory
        Returns
        -------
        tuple[str, str, str]
            (cmd, stdout, stderr)
        """
        if cwd:
            abs_cwd = os.path.join(self.cwd, cwd.format_map(self.params))
        else:
            abs_cwd = self.cwd
        process = subprocess.Popen(['bash'],
                                   cwd = abs_cwd,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        cmd = command.format_map(self.params)
        out, err = process.communicate(cmd)
        if err:
            self._log.warning(err)
        return cmd, out, err
    
    def execute_seq(self, commands: list[dict]) -> list[tuple[str, str, str]]:
        """Executes a whole sequence of bash commands
        
        Parameters
        ----------
        commands : list[dict]
            list of commands with optional cwd and out
        Returns
        -------
        list[tuple[str, str, str]]
            list of tuples (command, stdout, stderr)
        """
        ret = []
        for c in commands:
            self._log.info("$ %s", c["command"])
            cmd, out, err = self.execute(c["command"], c.get("cwd", ""))
            ret.append((cmd, out, err))
            self._log.info(">>> %s", out)
            if "out" in c:
                match = re.match(c["out"], out)
                if match:
                    self._log.info("ok")
        return ret
