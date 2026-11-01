import os, sys
_H = os.path.dirname(os.path.abspath(__file__))
for _p in (_H, os.path.join(_H, 'frozen')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
