import click

from click_help_colors import HelpColorsCommand, HelpColorsGroup


def test_error_color(runner):
    @click.command(
        cls=HelpColorsCommand,
        help_errors_color='red'
    )
    @click.option('--name', required=True)
    def cli(name):
        pass

    result = runner.invoke(cli, [], color=True)
    assert result.exit_code == 2
    assert result.output.splitlines() == [
        'Usage: cli [OPTIONS]',
        "Try 'cli --help' for help.",
        '',
        "\x1b[31mError\x1b[0m: Missing option '--name'.",
    ]


def test_error_color_default_unset(runner):
    @click.command(cls=HelpColorsCommand)
    @click.option('--name', required=True)
    def cli(name):
        pass

    result = runner.invoke(cli, [], color=True)
    assert result.exit_code == 2
    assert result.output.splitlines() == [
        'Usage: cli [OPTIONS]',
        "Try 'cli --help' for help.",
        '',
        "Error: Missing option '--name'.",
    ]


def test_error_color_inherited_from_group(runner):
    @click.group(
        cls=HelpColorsGroup,
        help_errors_color='red'
    )
    def cli():
        pass

    @cli.command()
    @click.option('--name', required=True)
    def sub(name):
        pass

    result = runner.invoke(cli, ['sub'], color=True)
    assert result.exit_code == 2
    assert result.output.splitlines() == [
        'Usage: cli sub [OPTIONS]',
        "Try 'cli sub --help' for help.",
        '',
        "\x1b[31mError\x1b[0m: Missing option '--name'.",
    ]


def test_error_color_no_color_env(runner, monkeypatch):
    monkeypatch.setenv('NO_COLOR', '1')

    @click.command(
        cls=HelpColorsCommand,
        help_errors_color='red'
    )
    @click.option('--name', required=True)
    def cli(name):
        pass

    result = runner.invoke(cli, [], color=True, env={'NO_COLOR': '1'})
    assert result.exit_code == 2
    assert result.output.splitlines() == [
        'Usage: cli [OPTIONS]',
        "Try 'cli --help' for help.",
        '',
        "Error: Missing option '--name'.",
    ]
