from pathlib import Path
import re

from src.exceptions import FileNotFound, NoShebangError


class _ScriptName:
    """Name of the script, wich is needed
    to organize scripts order"""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def is_number(cls, number: str) -> bool:
        try:
            int(number)
        except ValueError:
            return False
        return True

    def _find_last_underscore(self) -> int:
        return len(self.name) - self.name[::-1].find("_")

    def _find_last_dot(self) -> int:
        return len(self.name) - self.name[::-1].find(".") - 1

    def find_script_number(self) -> int:
        """Find number of the script in its name.
        If script is not numbered return empty string."""

        script_number = self.name[self._find_last_underscore() : self._find_last_dot()]

        if self.is_number(script_number):
            return int(script_number)

        return 0

    def is_script_numbered(self) -> bool:
        return bool(self.find_script_number())


class Script:
    """Script which know how to read  itself"""

    SHEBANG_REGEX = re.compile(r"#![/\\](?:(?!\.\s+)\S)+(\S)?(\.)?")

    def __init__(self, name: str, folder_path: Path):
        self.name = _ScriptName(name)
        self.path = folder_path.joinpath(name)

        if not self.path.exists():
            raise FileNotFound(f"{self.path} not found")

    def __iter__(self):
        """Create generator to yield script lines"""

        with open(self.path, "r") as script_file:

            while script_line := script_file.readline():

                yield script_line

    def __str__(self):
        return str(self.name)

    @classmethod
    def _find_shebang(cls, line: str) -> str:
        """Find shebang in line.
        If shebang is not exsisting return empty str.
        It is used by `is_shebang` to recognize  shebang lines."""
        if shebang := cls.SHEBANG_REGEX.match(line):
            return shebang.string
        return ""

    @classmethod
    def _extract_shebang_path(cls, line: str) -> str:
        """Slice string to create valid path (without shebang or newline)"""
        return line.replace("#!", "").replace("\n", "")

    @classmethod
    def _is_shebang(cls, line: str) -> bool:
        """Decide is line containing a shebang"""
        return bool(cls._find_shebang(line))

    def find_shebang_path(self) -> str:
        """Iterate script line by line to find shebang, when it is
        found extract interpreter path from it.

        Shebang example:
                #!/bin/bash

        If no shebang is found raise NoShebangError.
        """
        for line in self:
            if self._is_shebang(line):
                return self._extract_shebang_path(line)
        raise NoShebangError(f"No shebang found in {self.name}")
