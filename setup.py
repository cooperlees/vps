#!/usr/bin/env python3

from vps import __version__
from setuptools import setup


setup(
    name="vps",
    version=__version__,
    packages=["vps", "vps.tests"],
    url="http://github.com/cooperlees/vps",
    license="BSD 2-Clause",
    author="Cooper Lees",
    author_email="me@cooperlees.com",
    description="Webpage to run on my VPS instances",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: System Administrators",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=["aiohttp", "click"],
    entry_points={"console_scripts": ["vps = vps.main:main"]},
    test_suite="vps.tests.base",
)
