import os

import pytest

import click
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def clean_env():
    old = dict(os.environ)
    os.environ.pop("FORCE_COLOR", None)
    os.environ.pop("NO_COLOR", None)
    yield
    os.environ = old
