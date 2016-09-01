import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand


@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green'
)
def cli():
    pass

@cli.command()
@click.option('--count', default=1, help='Some number.')
def command1(count):
    click.echo('command 1')

@cli.command(
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option('--name', help='Some string.')
def command2(name):
    click.echo('command 2')


if __name__ == '__main__':
    cli()
