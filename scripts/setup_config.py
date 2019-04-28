#!/usr/bin/env python

import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.join(__DIR_PATH, '..')
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

from utils import config

DB_PATH = os.path.join(__DIR_PATH, '../data/amazonsharp.db')

config.set_value(config.DB_NAME, DB_PATH)
config.save()
