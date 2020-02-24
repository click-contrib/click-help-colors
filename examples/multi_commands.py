import click
from click_help_colors import HelpColorsGroup, HelpColorsMultiCommand


@click.group()
def cmd1():
    pass


@cmd1.command()
@click.option('--count', default=1, help='Some number.')
def command1(count):
    click.echo('command 1')


@click.group(
    cls=HelpColorsGroup,
    help_headers_color='red',
    help_options_color='blue'
)
def cmd2():
    pass


@cmd2.command()
@click.option('--name', help='Some string.')
def command2(name):
    click.echo('command 2')


class MyCLI(HelpColorsMultiCommand):
    def list_commands(self, ctx):
        return ['cmd1', 'cmd2']

    def get_command(self, ctx, name):
        return globals()[name]


@click.command(
    cls=MyCLI,
    help_headers_color='yellow',
    help_options_color='green'
)
def cli():
    pass


if __name__ == '__main__':
    cli()
