"""
This modules abstracts the access and modification of a config file in toml
format.
"""

from typing import Dict, Optional, TextIO
import os
import toml

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILENAME: str = 'config.toml'
CONFIG_PATH: str = os.path.join(__DIR_PATH, '..', CONFIG_FILENAME)

DB_NAME: str = 'dbName'


def __parse_config(filename: str) -> Dict[str, str]:
    """
    Parses the file with name, filename, into a dictionary.  Assumes the
    file content is in TOML format.
    """
    try:
        return toml.load(filename)
    except FileNotFoundError:
        return {}


__cfg: Dict[str, str] = __parse_config(CONFIG_PATH)


def get_value(name: str) -> Optional[str]:
    "Return the value for the key, name."
    return __cfg.get(name)


def set_value(name: str, value: str) -> None:
    "Set the value of the key, name, to value."
    __cfg[name] = value


def save() -> None:
    "Save the config to previously specified filename."
    file_handler: TextIO = open(CONFIG_PATH, 'w')
    toml.dump(__cfg, file_handler)


TEST_FILENAME: str = CONFIG_PATH
TEST_FILECONTENT: str = '''
title = "Example"

[owner]
name = "testing"
'''


def setup_file() -> None:
    """
    This function would setup the testing environment by creating a file with
    valid toml content.
    """
    with open(TEST_FILENAME, 'w') as file_handler:
        file_handler.write(TEST_FILECONTENT)

    global __cfg
    __cfg = __parse_config(TEST_FILENAME)


def teardown_file() -> None:
    "This function would remove the file created by setup_file."
    os.remove(TEST_FILENAME)


def test_get_value():
    "This function tests the get_value method."
    setup_file()
    assert get_value('title') == 'Example'
    teardown_file()


def test_set_value():
    "This function tests the set_value method."
    setup_file()
    set_value('test', 'bye')
    assert __cfg['test'] == 'bye'
    teardown_file()


def test_save_new():
    "This function tests the save method when filename doesn't exist."
    set_value('name', 'example')
    save()

    global __cfg
    old__cfg = __cfg
    __cfg = __parse_config(TEST_FILENAME)
    assert get_value('name') == 'example'
    __cfg = old__cfg

    teardown_file()


def test_save_old():
    "This function tests the save method when filename already exists."
    setup_file()
    set_value('test', 'bye')
    save()

    global __cfg
    old__cfg = __cfg
    __cfg = __parse_config(TEST_FILENAME)
    assert get_value('test') == 'bye'
    __cfg = old__cfg

    teardown_file()


def main():
    "Run all the tests in this module."
    test_get_value()
    test_set_value()
    test_save_old()
    test_save_new()


if __name__ == '__main__':
    main()
