#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

from setuptools import setup
import os

if os.getenv('READTHEDOCS'):
    with open('requirements_docs.txt') as f:
        required = f.read().splitlines()
    compile_ext = False
else:
    import numpy as np
    from Cython.Build import cythonize
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    compile_ext = True

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
]

args = dict(
    name='vzlog',
    version='0.1.8',
    url="https://github.com/gustavla/vzlog",
    description=("Python tool for logging rich content, "
                 "particularly plots and images"),
    author='Gustav Larsson',
    author_email='gustav.m.larsson@gmail.com',
    install_requires=required,
    packages=[
        'vzlog',
        'vzlog.image',
    ],
    license='BSD',
    classifiers=CLASSIFIERS,
)

if compile_ext:
    args['setup_requires'] = ['numpy', 'cython']
    args['ext_modules'] = cythonize("vzlog/image/resample.pyx")
    args['include_dirs'] = [np.get_include()]

setup(**args)
