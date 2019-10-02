import pytest

import click
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()
