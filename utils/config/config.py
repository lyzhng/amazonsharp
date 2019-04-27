"""
This modules abstracts the access and modification of a config file in toml
format.
"""

from typing import Dict, Optional, TextIO
import toml


class Config:
    "Class to represent a config file in memory."

    def __init__(self, filename: str):
        self.filename: str = filename
        self.config: Dict[str, str] = Config._parse_config(filename)

    @staticmethod
    def _parse_config(filename: str) -> Dict[str, str]:
        """
        Parses the file with name, filename, into a dictionary.  Assumes the
        file content is in TOML format.
        """
        try:
            return toml.load(filename)
        except FileNotFoundError:
            return {}

    def get_value(self, name: str) -> Optional[str]:
        "Return the value for the key, name."
        return self.config.get(name)

    def set_value(self, name: str, value: str) -> None:
        "Set the value of the key, name, to value"
        self.config[name] = value

    def save(self) -> None:
        "Save the config to previously specified filename."
        file_handler: TextIO = open(self.filename, 'w')
        toml.dump(self.config, file_handler)
