# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup


with io.open("click_help_colors/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)


setup(
    name='click-help-colors',
    version=version,
    packages=['click_help_colors'],
    description='Colorization of help messages in Click',
    url='https://github.com/r-m-n/click-help-colors',
    download_url='https://github.com/r-m-n/click-help-colors/archive/0.6.tar.gz',
    keywords=['click'],
    license='MIT',
    install_requires=[
        'click>=7.0'
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    }
)
