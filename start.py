#!/usr/bin/env python
"""
        Usage:
                start.py [-s SHELL] [-d SCRIPTS_DIRECTORY] [-o OUTPUT_CONTROLLER] [-e ERRORS_BUFFER_PATH]

        Options:
                -s SHELL                        Shell by which scripts will be executed.
                -d SCRIPTS_DIRECTORY            Directory with scripts which will be executed.
                -e ERRORS_BUFFER_PATH           Path to temporary errors file buffer. By default "/tmp".
                -o OUTPUT_CONTROLLER            Controll output format. See 'Choices' for possible options.


        Choices:

           * - default choice

                OUTPUT_CONTROLLERs:
                        1. terminal         print output to terminal.
                        2. terminalfile     print output to terminal and save it to files.
                       *3. terminalcolor    print output on green, success on blue, errors and fails on red.


                SHELLs:
                       *1. bash             execute scripts by /bin/bash .

"""
from pathlib import Path
import sys

from docopt import docopt

from src.app import main
from src.cli_utils import (
    parse_cli_output_input_controller,
    parse_cli_scripts_directory,
    parse_cli_errors_directory,
    parse_cli_shell,
    find_shell,
)
from src.output_input_controllers.controllers import TerminalOutputInputColor


if __name__ == "__main__":
    default_output_input_controller = TerminalOutputInputColor()

    # By default scripts are in ./scripts directory
    default_scripts_directory = Path(sys.argv[0]).parent.joinpath("scripts")

    # By default errors buffer is in /tmp directory
    default_error_buffer_directory = Path("/tmp")

    args = docopt(__doc__)

    output_input_controller = (
        parse_cli_output_input_controller(args) or default_output_input_controller
    )

    scripts_directory = parse_cli_scripts_directory(args) or default_scripts_directory

    shell = parse_cli_shell(args) or find_shell()

    errors_directory = (
        parse_cli_errors_directory(args) or default_error_buffer_directory
    )

    main(
        shell=shell,
        script_folder_path=scripts_directory,
        oi_controller=output_input_controller,
        errors_buffer_path=errors_directory,
    )
