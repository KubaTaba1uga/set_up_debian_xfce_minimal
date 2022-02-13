from datetime import datetime
from pathlib import Path
import sys
import os

from colorama import Fore, Style


NOW = datetime.now().isoformat()

INDENT = " " * 4

LOGS_DIR_NAME = "logs"

LOGS_DIR_PATH = Path(sys.argv[0]).parent.joinpath(LOGS_DIR_NAME)


def create_logs_dir():
    os.mkdir(LOGS_DIR_PATH)


def format_log_name(script_name: str) -> str:
    EXTENSION = ".log"
    return script_name + "_" + NOW + EXTENSION


def create_log_name(script_name: str) -> str:

    extension_index = len(script_name) - script_name[::-1].find(".") - 1

    if extension_index > 0:
        return format_log_name(script_name[:extension_index])

    return format_log_name(script_name)


def get_log_file_path(log_name: str) -> Path:

    return LOGS_DIR_PATH.joinpath(log_name)


def write_to_log(script_name: str, output: str):
    log_name = create_log_name(script_name)

    if not LOGS_DIR_PATH.exists():
        create_logs_dir()

    with open(get_log_file_path(log_name), "a") as f:
        f.write(output)


def write_to_summary(output: str):

    log_name = create_log_name("execution_summary")

    with open(get_log_file_path(log_name), "w") as f:
        f.write(output)


def format_error_output(output: str) -> str:
    return "ERROR: " + output


def color_info(output: str) -> str:
    """Color output in GREEN"""
    return Fore.GREEN + output + Style.RESET_ALL


def color_error(output: str) -> str:
    """Color output in RED"""
    return Fore.RED + output + Style.RESET_ALL


def color_success(output: str) -> str:
    """Color output in BLUE"""
    return Fore.BLUE + output + Style.RESET_ALL


def format_success(script_name: str) -> str:
    return format_indent(f"Execution of {script_name} succeed" + "\n")


def format_failure(script_name: str) -> str:
    return format_indent(f"Execution of {script_name} failed" + "\n")


def format_indent(output: str) -> str:
    """Add tab before output"""
    return INDENT + output


def print_(output: str):
    sys.stdout.write(Style.RESET_ALL + output + Style.RESET_ALL)
    sys.stdout.flush()


def print_info(output: str):
    """Print  informational notification in GREEN"""
    print_(color_info(output))


def print_error(output: str):
    """Print error notification in RED"""
    print_(color_error(output))


def print_success(output: str):
    """Print success notification in BLUE"""
    print_(color_success(output))


def ask_to_exit() -> bool:
    """If user would like to exit return True
    if not return False"""

    question = "Would You like to stop scripts execution? (y/[n]) "

    choices = {"yes": "y", "no": "n", "default": ""}

    while True:

        anwser = input(question)

        if anwser in choices.values():
            return anwser == choices["yes"]

        else:
            print_("\n" + "Wrong input value!!! Type 'y' or 'n'" + "\n" * 2)
