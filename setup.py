# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup


with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()


with io.open("click_help_colors/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)


setup(
    name='click-help-colors',
    version=version,
    packages=['click_help_colors'],
    description='Colorization of help messages in Click',
    long_description=readme,
    url='https://github.com/r-m-n/click-help-colors',
    keywords=['click'],
    license='MIT',
    install_requires=[
        'click>=7.0,<8'
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    }
)
