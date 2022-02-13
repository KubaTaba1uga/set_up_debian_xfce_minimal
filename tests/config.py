from contextlib import contextmanager
from pathlib import Path
from io import StringIO
import shutil
import sys
import os

GOOD_SCRIPTS_DIR = Path("./tests/scripts/good_scripts")

BAD_SCRIPTS_DIR = Path("./tests/scripts/bad_scripts")

ERRORS_BUFFER_DIR = Path("/tmp")

SCRIPT_WITH_NUMBER_NAME = "my_script_-1.sh"

SCRIPT_WITHOUT_NUMBER_NAME = "my_script.sh"

GOOD_SCRIPTS = {
    "shebang": {"name": "bash_shebang_0.sh", "shebang_path": "/bin/bash"},
    "input": {"name": "bash_input_1.sh"},
    "error": {"name": "bash_error_3.sh"},
    "output": {"name": "bash_output_4.sh"},
    "dir_path": GOOD_SCRIPTS_DIR,
}

BAD_SCRIPTS = {
    "no_shebang": {"name": "bash_no_shebang.sh", "shebang_path": ""},
    "create_file": {"name": "create_file.sh"},
    "echo": {"name": "bash_echo_This_is_standard_notification.sh"},
    "error": {"name": "bash_error.sh"},
    "dir_path": BAD_SCRIPTS_DIR,
}


@contextmanager
def replace_stdin(notification):
    org_stdin = sys.stdin
    sys.stdin = StringIO(notification)
    yield None
    sys.stdin = org_stdin


@contextmanager
def open_log_with_cleanup(file_path: Path, mode: str = "r"):
    """Delete log files and theirs parent directory after usage"""
    f = open(file_path, mode)
    yield f
    f.close()
    shutil.rmtree(file_path.parent)
