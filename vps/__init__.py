#!/usr/bin/env python3

from collections import namedtuple

__version_info__ = namedtuple(
    'version_info',
    'major minor micro releaselevel serial')(major=0,
                                             minor=6,
                                             micro=9,
                                             releaselevel='alpha',
                                             serial=69)

__version__ = '{v.major}.{v.minor}.{v.micro}'.format(v=__version_info__)
