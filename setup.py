#!/usr/bin/env python

from distutils.core import setup

CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
"""

setup(name='vzlog',
    version='0.1',
    url="https://github.com/gustavla/vzlog",
    description="Python tool for logging rich content, "
                "particularly plots and images",
    author='Gustav Larsson',
    packages=[
        'vzlog',
    ],
    license = 'BSD',
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    )
)
