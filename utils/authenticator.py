import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.join(__DIR_PATH, '../..')

if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)


def is_logged_in(admin_required: bool = False, seller_required: bool = False,
                 developer_required: bool = False):
    pass


def login_required(admin_required: bool = False, seller_required: bool = False,
                   developer_required: bool = False):
    pass
