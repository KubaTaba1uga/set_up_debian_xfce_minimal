from src.output_input_controllers.base import OutputInputController
from src.output_input_controllers.descriptors import (
    SimpleTerminalInputDescriptor,
    TerminalOutputDescriptorColor,
    TerminalFileOutputDescriptor,
    TerminalErrorDescriptorColor,
    TerminalFileErrorDescriptor,
    TerminalOutputDescriptor,
    TerminalErrorDescriptor,
)
from src.output_input_controllers.utils import (
    write_to_summary,
    format_success,
    format_failure,
    print_success,
    print_error,
)


class TerminalOutputInput(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()

    command_line_argument = "terminal"


class TerminalOutputInputColor(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptorColor()
    stderr = TerminalErrorDescriptorColor()

    command_line_argument = "terminalcolor"

    @classmethod
    def show_success(cls, script_name: str):
        print_success(format_success(script_name))

    @classmethod
    def show_failure(cls, script_name: str):
        print_error(format_failure(script_name))


class TerminalFileOutputInput(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalFileOutputDescriptor()
    stderr = TerminalFileErrorDescriptor()

    command_line_argument = "terminalfile"

    @classmethod
    def show_progress(cls):
        super().show_progress()

        output = "Scripts Summary:" + "\n" * 2

        for script in cls.scripts_statuses:
            for script_name, exit_code in script.items():
                if exit_code == 0:
                    output += format_success(script_name)
                else:
                    output += format_failure(script_name)

        write_to_summary(output)
