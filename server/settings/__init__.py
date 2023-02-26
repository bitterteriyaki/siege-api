"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from pathlib import Path

from decouple import AutoConfig

# Your Django project directory. It is the directory that contains your
# `manage.py` file.

BASE_DIR = Path(__file__).parent.parent.parent

# Configuration for the decouple library. It is used to read environment
# variables from a `.env` file.
# https://github.com/HBNetwork/python-decouple

config = AutoConfig(search_path=BASE_DIR.joinpath("config"))
