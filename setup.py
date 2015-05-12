#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
]

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='vzlog',
    version='0.1.2',
    url="https://github.com/gustavla/vzlog",
    description=("Python tool for logging rich content, "
                 "particularly plots and images"),
    author='Gustav Larsson',
    author_email='gustav.m.larsson@gmail.com',
    install_requires=required,
    packages=[
        'vzlog',
    ],
    license='BSD',
    classifiers=CLASSIFIERS,
)
