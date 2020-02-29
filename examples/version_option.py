import click
from click_help_colors import version_option


@click.group()
def cli():
    pass

@cli.command()
@version_option(
    version='1.0',
    prog_name='example',
    message_color='green'
)
def cmd1():
    pass

@cli.command()
@version_option(
    version='1.0',
    prog_name='example',
    version_color='green',
    prog_name_color='yellow'
)
def cmd2():
    pass

@cli.command()
@version_option(
    version='1.0',
    prog_name='example',
    version_color='green',
    prog_name_color='white',
    message='%(prog)s %(version)s\n   python=3.7',
    message_color='bright_black'
)
def cmd3():
    pass


if __name__ == '__main__':
    cli()
