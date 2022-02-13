import pytest

from src.script import Script
from src.exceptions import NoShebangError, FileNotFound

from tests.config import GOOD_SCRIPTS


def test_script__init__error(non_existing_path):
    with pytest.raises(FileNotFound):
        Script(GOOD_SCRIPTS["shebang"]["name"], non_existing_path)


def test_script_iteration(script_shebang):
    """Check is object iterable"""
    with open(script_shebang.path) as script_file:
        for line in script_shebang:
            assert line == script_file.readline()


def test_script_find_shebang_path(script_shebang):
    assert script_shebang.find_shebang_path() == GOOD_SCRIPTS["shebang"]["shebang_path"]


def test_script_cant_find_shebang_path(script_no_shebang):
    with pytest.raises(NoShebangError):
        script_no_shebang.find_shebang_path()
