import pytest

from src.script_executor import ScriptExecutor
from src.exceptions import ShellNotSpawned
from tests.config import replace_stdin


def test__init__errors(bash_output_script, bash_shell, terminal_oi, temp_err_buffer):
    with pytest.raises(TypeError):
        ScriptExecutor("it is not script", bash_shell, terminal_oi, temp_err_buffer)

    with pytest.raises(TypeError):
        ScriptExecutor(
            bash_output_script, "this is not shell", terminal_oi, temp_err_buffer
        )

    with pytest.raises(TypeError):
        ScriptExecutor(
            bash_output_script,
            bash_shell,
            "this is not output input controller",
            temp_err_buffer,
        )

    with pytest.raises(ShellNotSpawned):
        ScriptExecutor(bash_output_script, bash_shell, terminal_oi, temp_err_buffer)


def test_pid(script_executor):
    pid_command = script_executor.shell.create_subshell_pid_command()
    with script_executor.shell as sh:
        sh.send_command(pid_command)
        assert isinstance(script_executor.pid, int)


def test_exit_code(script_executor):
    command = "ls"
    with script_executor.shell as sh:
        sh.send_command(command)
        assert script_executor.exit_code == 0


def test__create_execution_command(script_executor):
    command = script_executor._create_execution_command()
    with script_executor.shell as sh:
        sh.send_command(command)
        assert isinstance(script_executor.pid, int)
        assert script_executor.exit_code == 0


def test_get_output(script_executor_output):
    OUTPUT = "This is standard notification"
    command = script_executor_output._create_execution_command()
    output_not_found = True

    with script_executor_output.shell as sh:
        sh.send_command(command)

        i = 0

        while output_not_found:

            script_executor_output.get_output()

            stdout = script_executor_output.oi_controller.stdout

            if OUTPUT in stdout:
                output_not_found = False
                break

            # Allow only for 1000 checks
            if i < 1000:
                i += 1
            else:
                break

        assert output_not_found is False


def test_get_error(script_executor_error):
    ERROR = "ls: cannot access"

    command = script_executor_error._create_execution_command()
    error_not_found = True

    with script_executor_error.shell as sh:
        sh.send_command(command)

        i = 0

        while error_not_found:

            script_executor_error.get_errors()
            try:
                if ERROR in script_executor_error.oi_controller.stderr:
                    error_not_found = False
                    break
            except KeyError:
                pass

            # Allow only for 1000 checks
            if i < 1000:
                i += 1
            else:
                break

        assert error_not_found is False


def test_get_input(script_executor_input):
    INPUT = "This is standard input notification"
    command = script_executor_input._create_execution_command()

    with replace_stdin(INPUT):
        with script_executor_input.shell as sh:
            sh.send_command(command)

            script_executor_input.get_input()

            assert INPUT in script_executor_input.oi_controller.stdin
