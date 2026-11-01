import os
import sys

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import _boot  # noqa: E402,F401
