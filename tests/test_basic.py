import click
import pytest

from click_help_colors import HelpColorsGroup, HelpColorsException


def test_basic_group(runner):
    @click.command(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green'
    )
    @click.option('--name', help='The person to greet.')
    def cli(count):
        pass

    result = runner.invoke(cli, ['--help'], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        '\x1b[33mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...',
        '',
        '\x1b[33mOptions\x1b[0m:',
        '  \x1b[32m--name TEXT\x1b[0m  The person to greet.',
        '  \x1b[32m--help\x1b[0m       Show this message and exit.'
    ]


def test_basic_command(runner):
    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green'
    )
    def cli():
        pass

    @cli.command()
    @click.option('--name', help='The person to greet.')
    def command(name):
        pass

    result = runner.invoke(cli, ['--help'], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        '\x1b[33mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...',
        '',
        '\x1b[33mOptions\x1b[0m:',
        '  \x1b[32m--help\x1b[0m  Show this message and exit.',
        '',
        '\x1b[33mCommands\x1b[0m:',
        '  \x1b[32mcommand\x1b[0m'
    ]

    result = runner.invoke(cli, ['command', '--help'], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        '\x1b[33mUsage\x1b[0m: cli command [OPTIONS]',
        '',
        '\x1b[33mOptions\x1b[0m:',
        '  \x1b[32m--name TEXT\x1b[0m  The person to greet.',
        '  \x1b[32m--help\x1b[0m       Show this message and exit.'
    ]


def test_unknown_color(runner):
    @click.command(
        cls=HelpColorsGroup,
        help_headers_color='unknwnclr'
    )
    @click.option('--name', help='The person to greet.')
    def cli(count):
        pass

    result = runner.invoke(cli, ['--help'], color=True)
    assert result.exception
    assert isinstance(result.exception, HelpColorsException)
    assert str(result.exception) == "Unknown color 'unknwnclr'"


def test_env_no_color(runner):
    @click.command(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green'
    )
    @click.option('--name', help='The person to greet.')
    def cli(count):
        pass

    result = runner.invoke(cli, ['--help'], color=True, env={'NO_COLOR': '1'})
    assert not result.exception
    assert result.output.splitlines() == [
        'Usage: cli [OPTIONS] COMMAND [ARGS]...',
        '',
        'Options:',
        '  --name TEXT  The person to greet.',
        '  --help       Show this message and exit.'
    ]
