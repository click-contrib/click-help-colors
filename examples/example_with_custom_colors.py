import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand


@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
    help_options_custom_colors={'command3': 'red', 'command4': 'cyan'}
)
def cli():
    pass


@cli.command(
    cls=HelpColorsCommand,
    help_headers_color=None,
    help_options_color=None,
    help_options_custom_colors={'--count': 'red', '--subtract': 'green'}
)
@click.option('--count', default=1, help='Count help text.')
@click.option('--add', default=1, help='Add help text.')
@click.option('--subtract', default=1, help='Subtract help text.')
def command1(count, add, subtract):
    """A command"""
    click.echo('command 1')


@cli.command()
@click.option('--name', help='Some string.')
def command2(name):
    """Another command"""
    click.echo('command 2')


@cli.command()
@click.option('--name', help='Some string.')
def command3(name):
    """Yet another command"""
    click.echo('command 3')


@cli.command()
@click.option('--name', help='Some string.')
def command4(name):
    """One last command"""
    click.echo('command 4')


if __name__ == '__main__':
    cli()
