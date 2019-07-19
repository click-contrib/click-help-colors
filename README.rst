=================
click-help-colors
=================

Colorization of help messages in Click_.

Usage
-----

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

.. code-block:: console

    $ python example.py --help

.. image:: https://raw.githubusercontent.com/r-m-n/click-help-colors/master/examples/1.png

.. code-block:: console

    $ python example.py command1 --help

.. image:: https://raw.githubusercontent.com/r-m-n/click-help-colors/master/examples/2.png

.. code-block:: console

    $ python example.py command2 --help

.. image:: https://raw.githubusercontent.com/r-m-n/click-help-colors/master/examples/3.png

.. code:: python

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

  ...

.. code-block:: console

    $ python example_with_custom_colors.py --help

.. image:: https://raw.githubusercontent.com/r-m-n/click-help-colors/master/examples/4.png

.. code-block:: console

    $ python example_with_custom_colors.py --help

.. image:: https://raw.githubusercontent.com/r-m-n/click-help-colors/master/examples/5.png
  
Installation
------------

With ``pip``:

.. code-block:: console

    $ pip install click-help-colors

From source:

.. code-block:: console

    $ git clone https://github.com/r-m-n/click-help-colors.git
    $ cd click-help-colors
    $ python setup.py install

.. _Click: http://click.pocoo.org/
