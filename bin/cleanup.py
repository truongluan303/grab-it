#!/usr/bin/env python3

# A small python script to clean up cached files

import pathlib

[p.unlink() for p in pathlib.Path(".").rglob("*.py[co]")]
[p.rmdir() for p in pathlib.Path(".").rglob("__pycache__")]
