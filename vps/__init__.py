#!/usr/bin/env python3

from collections import namedtuple

__version_info__ = namedtuple("version_info", "major minor micro releaselevel serial")(
    major=2019, minor=7, micro=20, releaselevel="", serial=69
)

if __version_info__.releaselevel:
    __version__ = "{v.major}.{v.minor}.{v.micro}.{v.releaselevel}".format(
        v=__version_info__
    )
else:
    __version__ = "{v.major}.{v.minor}.{v.micro}".format(v=__version_info__)
