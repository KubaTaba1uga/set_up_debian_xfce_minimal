class FileNotFound(FileExistsError):
    pass


class FileNotExecutable(PermissionError):
    pass


class NoOutputProduced(Exception):
    pass


class NoShebangError(Exception):
    """Error is caused by absence of shebang inside a script.
    What is shebang??
            Shebang is interpreter directive with syntax:
                    #! <interpreter path> [optional-arg]
    """


class NoPidError(Exception):
    """No pid were generated before process execution"""


class NoExitCodeError(Exception):
    """No exit code were produced by process"""


class ShellNotSpawned(Exception):
    """Passed not spawned shell to class which require spawned one"""
