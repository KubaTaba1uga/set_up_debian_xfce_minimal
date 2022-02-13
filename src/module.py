from typing import Any
import pathlib
import os


from src.script import Script


class Module:
    """Collection of scripts"""

    def __init__(self, scripts_folder: pathlib.Path):
        self.scripts_folder = scripts_folder

    def __iter__(self):
        return (script[1] for script in self._list_sorted_scripts())

    @classmethod
    def _get_first_element(cls, collection: Any) -> Any:
        """Get first element of collection"""
        return collection[0]

    def _list_scripts(self) -> list:
        return [
            Script(script, self.scripts_folder)
            for script in os.listdir(self.scripts_folder)
            # Avoid executing hidden files
            if script[0] != "."
        ]

    def _list_sorted_scripts(self) -> list:
        scripts_list = self._list_scripts()

        for i, script in enumerate(scripts_list):

            scripts_list[i] = (
                script.name.find_script_number(),
                script,
            )

        scripts_list.sort(key=self._get_first_element)

        return scripts_list
