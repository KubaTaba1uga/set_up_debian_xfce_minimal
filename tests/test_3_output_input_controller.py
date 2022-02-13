from colorama import Fore

from src.output_input_controllers.utils import get_log_file_path, create_log_name

from tests.config import replace_stdin, open_log_with_cleanup


def test_terminal_oi_stdout(script_executor_terminal_oi, capfd):
    OUTPUT = "This is standard output notification"
    script_executor = script_executor_terminal_oi

    with script_executor.shell:
        script_executor.oi_controller.stdout = script_executor, OUTPUT
        out, err = capfd.readouterr()
        assert OUTPUT in out


def test_terminal_oi_stdin(script_executor_terminal_oi):
    INPUT = "This is standard input notification"
    script_executor = script_executor_terminal_oi

    with replace_stdin(INPUT):
        with script_executor.shell:
            script_executor.oi_controller.stdin = script_executor, None

    assert script_executor.oi_controller.stdin == INPUT


def test_terminal_oi_stderr(script_executor_terminal_oi, capfd):
    ERROR = "This is standard output notification"
    script_executor = script_executor_terminal_oi

    with script_executor.shell:
        script_executor.oi_controller.stdout = script_executor, ERROR
        out, err = capfd.readouterr()
        assert ERROR in out


def test_terminal_color_oi_stdout(script_executor_terminal_color_oi, capfd):
    OUTPUT = Fore.GREEN + "This is standard output notification"
    script_executor = script_executor_terminal_color_oi

    with script_executor.shell:
        script_executor.oi_controller.stdout = script_executor, OUTPUT
        out, err = capfd.readouterr()
        assert OUTPUT in out


def test_terminal_color_oi_stdin(script_executor_terminal_color_oi):
    INPUT = "This is standard input notification"
    script_executor = script_executor_terminal_color_oi

    with replace_stdin(INPUT):
        with script_executor.shell:
            script_executor.oi_controller.stdin = script_executor, None

    assert script_executor.oi_controller.stdin == INPUT


def test_terminal_color_oi_stderr(script_executor_terminal_color_oi, capfd):
    ERROR = Fore.RED + "This is standard output notification"
    script_executor = script_executor_terminal_color_oi

    with script_executor.shell:
        script_executor.oi_controller.stdout = script_executor, ERROR
        out, err = capfd.readouterr()
        assert ERROR in out


def test_terminal_file_oi_stdout(script_executor_terminal_file_oi, capfd):
    OUTPUT = "This is standard output notification"

    script_executor = script_executor_terminal_file_oi

    log_name = create_log_name(str(script_executor.script))

    log_path = get_log_file_path(log_name)

    with script_executor.shell:
        script_executor.oi_controller.stdout = script_executor, OUTPUT
        out, err = capfd.readouterr()
        assert OUTPUT in out
        with open_log_with_cleanup(log_path) as f:
            assert OUTPUT in f.read()


def test_terminal_file_oi_stdin(script_executor_terminal_file_oi):
    INPUT = "This is standard input notification"
    script_executor = script_executor_terminal_file_oi

    with replace_stdin(INPUT):
        with script_executor.shell:
            script_executor.oi_controller.stdin = script_executor, None

    assert script_executor.oi_controller.stdin == INPUT


def test_terminal_file_oi_stderr(script_executor_terminal_file_oi, capfd):
    ERROR = "This is standard error notification"

    script_executor = script_executor_terminal_file_oi

    log_name = create_log_name(str(script_executor.script))

    log_path = get_log_file_path(log_name)

    with script_executor.shell:
        script_executor.oi_controller.stderr = script_executor, ERROR
        out, err = capfd.readouterr()
        assert ERROR in out
        with open_log_with_cleanup(log_path) as f:
            assert ERROR in f.read()
