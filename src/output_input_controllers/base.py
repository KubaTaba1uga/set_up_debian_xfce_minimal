from typing import TYPE_CHECKING
from typing import Tuple, List, Dict
import abc

from src.output_input_controllers.utils import (
    format_success,
    format_failure,
    ask_to_exit,
    print_,
)

if TYPE_CHECKING:
    from src.script_executor import ScriptExecutor


class BaseDescriptor(abc.ABC):
    def __set_name__(self, cls, name: str):
        self.name = name

    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        """Receive shell, value and subshell PID
        to allow OutputInputController children
        for controlling processes behaviour"""

        _script_executor, str_value = values

        instance.__dict__[self.name] = str_value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class OutputInputController(abc.ABC):
    """Class responsible for handling terminal streams.
            Responsibilities description:

                receiving stdin and deciding what to do
                    with process that input was received from

                receiving stdout and deciding what to do
                    with process that output was received from

                receiving stderr and deciding what to do
                    with process that error was received from

    Use descriptors to override abstract class properties.
    """

    scripts_statuses: List[Dict[str, int]] = []

    @classmethod
    def show_success(cls, script_name: str):
        print_(format_success(script_name))

    @classmethod
    def show_failure(cls, script_name: str):
        print_(format_failure(script_name))

    @classmethod
    def ask_to_exit(cls, script_name: str):
        if ask_to_exit():
            exit(-1)

    @classmethod
    def show_progress(cls):
        print("\n" * 2 + "Scripts Summary:")

        for script in cls.scripts_statuses:
            for script_name, exit_code in script.items():
                if exit_code == 0:
                    cls.show_success(script_name)
                else:
                    cls.show_failure(script_name)

        print(end="\n" * 2)

    @classmethod
    def show_status(cls, script_executor: "ScriptExecutor"):

        script_name = str(script_executor.script)
        exit_code = script_executor.exit_code

        cls.scripts_statuses.append({script_name: exit_code})

        cls.show_progress()

        if exit_code != 0:
            cls.ask_to_exit(script_name)

    @property
    @classmethod
    def command_line_argument(cls) -> str:
        """Argument that user passes at script execution to select output input controller,
        for example: python start.py -o outputinputcontroller
        """
        return cls.__name__.lower()

    @classmethod
    @property
    @abc.abstractmethod
    def stdin(cls) -> BaseDescriptor:
        return BaseDescriptor()

    @classmethod
    @property
    @abc.abstractmethod
    def stdout(cls) -> BaseDescriptor:
        return BaseDescriptor()

    @classmethod
    @property
    @abc.abstractmethod
    def stderr(cls) -> BaseDescriptor:
        return BaseDescriptor()
