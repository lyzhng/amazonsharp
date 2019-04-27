"""
This module is for testing the config module.
"""


import os
import config


TEST_FILENAME: str = 'testfile'
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


def teardown_file() -> None:
    "This function would remove the file created by setup_file."
    os.remove(TEST_FILENAME)


def test_get_value():
    "This function tests the get_value method."
    setup_file()
    cfg = config.Config(TEST_FILENAME)
    assert cfg.get_value('title') == 'Example'
    teardown_file()


def test_set_value():
    "This function tests the set_value method."
    setup_file()
    cfg = config.Config(TEST_FILENAME)
    cfg.set_value('test', 'bye')
    assert cfg.config['test'] == 'bye'
    teardown_file()


def test_save_new():
    "This function tests the save method when filename doesn't exist."
    cfg = config.Config(TEST_FILENAME)
    cfg.set_value('name', 'example')
    cfg.save()

    new_cfg = config.Config(TEST_FILENAME)
    assert new_cfg.get_value('name') == 'example'

    teardown_file()


def test_save_old():
    "This function tests the save method when filename already exists."
    setup_file()
    cfg = config.Config(TEST_FILENAME)
    cfg.set_value('test', 'bye')
    cfg.save()

    new_cfg = config.Config(TEST_FILENAME)
    assert new_cfg.get_value('test') == 'bye'

    teardown_file()


def main():
    "Run all the tests in this module."
    test_get_value()
    test_set_value()
    test_save_old()
    test_save_new()


if __name__ == '__main__':
    main()
