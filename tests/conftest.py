from subprocess import Popen
from pathlib import Path
import pytest

from src.temporary_errors_buffer import TempErrorFile
from src.output_input_controllers.controllers import (
    TerminalOutputInputColor,
    TerminalFileOutputInput,
    TerminalOutputInput,
)
from src.script_executor import ScriptExecutor
from src.script import _ScriptName
from src.shell import BashShell
from src.module import Module
from src.script import Script

from tests.config import (
    SCRIPT_WITHOUT_NUMBER_NAME,
    SCRIPT_WITH_NUMBER_NAME,
    ERRORS_BUFFER_DIR,
    GOOD_SCRIPTS,
    BAD_SCRIPTS,
)


@pytest.fixture
def bash_output_script():
    return Script(GOOD_SCRIPTS["output"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def script_shebang():
    return Script(GOOD_SCRIPTS["shebang"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def script_input():
    return Script(GOOD_SCRIPTS["input"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def script_no_shebang():
    return Script(BAD_SCRIPTS["no_shebang"]["name"], BAD_SCRIPTS["dir_path"])


@pytest.fixture
def script_error():
    return Script(BAD_SCRIPTS["error"]["name"], BAD_SCRIPTS["dir_path"])


@pytest.fixture
def script_echo():
    return Script(BAD_SCRIPTS["echo"]["name"], BAD_SCRIPTS["dir_path"])


@pytest.fixture
def bash_shell():
    return BashShell()


@pytest.fixture
def popen_process():
    return Popen(args=["/usr/bin/sleep", "10"])


@pytest.fixture
def module():
    return Module(GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def script_name_with_number():
    return _ScriptName(SCRIPT_WITH_NUMBER_NAME)


@pytest.fixture
def script_name_without_number():
    return _ScriptName(SCRIPT_WITHOUT_NUMBER_NAME)


@pytest.fixture
def non_existing_path():
    path = "/xyz/cxz/zxc/xcz"
    return Path(path)


@pytest.fixture
def non_executable_path():
    path = "/bin"
    return Path(path)


@pytest.fixture
def terminal_oi():
    return TerminalOutputInput()


@pytest.fixture
def terminal_color_oi():
    return TerminalOutputInputColor()


@pytest.fixture
def terminal_file_oi():
    return TerminalFileOutputInput()


@pytest.fixture
def temp_err_buffer():
    return TempErrorFile(ERRORS_BUFFER_DIR)


@pytest.fixture
def script_executor(bash_shell, bash_output_script, terminal_oi, temp_err_buffer):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(bash_output_script, bash_shell, terminal_oi, temp_err_buffer)


@pytest.fixture
def script_executor_terminal_oi(
    bash_shell, bash_output_script, terminal_oi, temp_err_buffer
):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(bash_output_script, bash_shell, terminal_oi, temp_err_buffer)


@pytest.fixture
def script_executor_terminal_color_oi(
    bash_shell, bash_output_script, terminal_color_oi, temp_err_buffer
):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(
        bash_output_script, bash_shell, terminal_color_oi, temp_err_buffer
    )


@pytest.fixture
def script_executor_terminal_file_oi(
    bash_shell, bash_output_script, terminal_file_oi, temp_err_buffer
):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(
        bash_output_script, bash_shell, terminal_file_oi, temp_err_buffer
    )


@pytest.fixture
def script_executor_error(bash_shell, script_error, terminal_oi, temp_err_buffer):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(script_error, bash_shell, terminal_oi, temp_err_buffer)


@pytest.fixture
def script_executor_output(bash_shell, script_echo, terminal_oi, temp_err_buffer):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(script_echo, bash_shell, terminal_oi, temp_err_buffer)


@pytest.fixture
def script_executor_input(bash_shell, script_input, terminal_oi, temp_err_buffer):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(script_input, bash_shell, terminal_oi, temp_err_buffer)
