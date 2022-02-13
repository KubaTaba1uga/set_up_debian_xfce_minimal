from typing import Optional
from select import select
import sys

from src.output_input_controllers.base import OutputInputController
from src.temporary_errors_buffer import TempErrorFile
from src.exceptions import ShellNotSpawned
from src.process import Process
from src.shell import SubShell
from src.script import Script


class ScriptExecutor:
    def __init__(
        self,
        script: Script,
        shell: SubShell,
        oi_controller: OutputInputController,
        errors_buffer: TempErrorFile,
    ):
        if not isinstance(script, Script):
            raise TypeError("script has to be Script type")

        if not isinstance(shell, SubShell):
            raise TypeError("shell has to subclass of SubShell")

        if not isinstance(oi_controller, OutputInputController):
            raise TypeError("oi_controller has to be subclass of OutputInputController")

        if not shell.process:
            raise ShellNotSpawned(f"Passed not spawned shell for {script} execution")

        self.script = script
        self.shell = shell
        self.oi_controller = oi_controller
        self.errors_buffer = errors_buffer
        self._pid: Optional[int] = None
        self._exit_code: Optional[int] = None

    @property
    def pid(self) -> int:
        """Get PID of script in shell output"""
        if not self._pid:
            self._pid = self.shell.find_subshell_pid()
        return self._pid

    @property
    def exit_code(self) -> int:
        """Get exit code of last executed process"""
        if not self._exit_code:
            self._exit_code = self.shell.get_subshell_exit_code()
        return self._exit_code

    def _create_execution_command(self) -> str:
        """Create subshell and return its PID. Script
        will be executed within a subshell by command
        syntax.

        Generated PID will be used to recognize process status
        like:
                terminated
                hang up
                suspend
        """

        pid_command, interpreter_path, script_path, error_redirection = (
            self.shell.create_subshell_pid_command(),
            self.script.find_shebang_path(),
            self.script.path,
            self.errors_buffer.create_error_redirection(),
        )

        return (
            # SubShell char start
            self.shell.subshell["start"]
            # Create pid before execution
            + f"{pid_command} && "
            # Execute under the pid
            + f"exec {interpreter_path} "
            # Script which will be executed
            + f"{script_path}"
            # Redirect errors to temporary file
            + f"{error_redirection}"
            # SubShell char end
            + self.shell.subshell["end"]
        )

    def get_output(self):
        """Get output from shell and pass it to
        output input controller"""
        output = self.shell.read_output_line()
        self.oi_controller.stdout = self, output

    def get_errors(self):
        """Get errors from errors temporary file
        and pass it to output input controller"""
        if self.errors_buffer.exist():
            self.oi_controller.stderr = (
                self,
                self.errors_buffer.read(),
            )

    def get_input(self):
        """Get input from user and pass it to shell"""
        self.oi_controller.stdin = self, ""

    def execute_script(self):
        """Execute script as separeted process"""

        command = self._create_execution_command()

        self.shell.send_command(command)

        pid = self.pid

        with self.errors_buffer:

            while Process.is_alive(pid) or self.shell.lastline:
                # Create event loop for blocking
                #    input/output operations
                readers, writers, _ = select([sys.stdin], [sys.stdout], [], 1)
                for fd in readers + writers:
                    if fd is sys.stdin:
                        self.get_input()
                    elif fd is sys.stdout:
                        self.get_output()
                self.get_errors()

            self.oi_controller.show_status(self)
