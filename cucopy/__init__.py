"""
**CuCoPy** is a Python library for adjusting euro values for inflation.
"""

__version__ = "0.1.5"
__author__ = 'Julian Schönau'

import os, pathlib

DATASET_PATH = os.path.join(os.path.join(pathlib.Path(__file__).parent.resolve(), 'data'))
