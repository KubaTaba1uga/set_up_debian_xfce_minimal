from typing import Tuple, TYPE_CHECKING
import sys


from src.output_input_controllers.base import BaseDescriptor
from src.output_input_controllers.utils import (
    format_error_output,
    write_to_log,
    print_error,
    print_info,
    print_,
)

if TYPE_CHECKING:
    from src.script_executor import ScriptExecutor


class SimpleTerminalInputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        script_executor, _ = values

        line = sys.stdin.readline()

        script_executor.shell.send_command(line)  # type:ignore

        instance.__dict__[self.name] = line


class TerminalOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_(str_value)

        instance.__dict__[self.name] = str_value


class TerminalOutputDescriptorColor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_info(str_value)

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_(format_error_output(str_value))

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptorColor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_error(format_error_output(str_value))

        instance.__dict__[self.name] = str_value


class TerminalFileOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        script_executor, str_value = values

        write_to_log(str(script_executor.script), str_value)

        print_(str_value)

        instance.__dict__[self.name] = str_value


class TerminalFileErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        script_executor, str_value = values

        errors = format_error_output(str_value)

        write_to_log(str(script_executor.script), errors)

        print_(errors)

        instance.__dict__[self.name] = str_value
