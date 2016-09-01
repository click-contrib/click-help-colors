=================
click-help-colors
=================

Colorization of help messages in a click_.

Usage:

.. code:: python

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

$ python example.py --help

.. image:: https://github.com/r-m-n/click-help-colors/blob/master/examples/1.png

$ python example.py command1 --help

.. image:: https://github.com/r-m-n/click-help-colors/blob/master/examples/2.png

$ python example.py command2 --help

.. image:: https://github.com/r-m-n/click-help-colors/blob/master/examples/3.png


.. _click: http://click.pocoo.org/
