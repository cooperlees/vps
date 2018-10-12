#!/usr/bin/env python3

from collections import namedtuple

__version_info__ = namedtuple("version_info", "major minor micro releaselevel serial")(
    major=2018, minor=10, micro=12, releaselevel="alpha", serial=69
)

__version__ = "{v.major}.{v.minor}.{v.micro}".format(v=__version_info__)
