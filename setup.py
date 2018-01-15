#!/usr/bin/env python
import os
import sys
import re

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# Handle encoding
major, minor1, minor2, release, serial = sys.version_info
if major >= 3:
    def rd(filename):
        f = open(filename, encoding="utf-8")
        r = f.read()
        f.close()
        return r
else:
    def rd(filename):
        f = open(filename)
        r = f.read()
        f.close()
        return r

setup(
    name='wolfie',
    packages =['wolfie'],
    version="0.1.1",
    author='John Livingston',
    author_email = 'jliv84@gmail.com',
    url = 'https://github.com/john-livingston/wolfie',
    license = ['GNU GPLv3'],
    description ='Interface to the M-R relation code from Wolfgang+2015',
    long_description=rd("README.md") + "\n\n"
                    + "---------\n\n",
    package_dir={"wolfie": "wolfie"},
    package_data={"wolfie": ["R/posterior_samples.savr", "R/calc_mass_postpred.R"]},
    scripts=['scripts/wolfie'],
    include_package_data=True,
    keywords=['M-R'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python'
        ],
    install_requires = ['numpy', 'pandas', 'rpy2'],
)
