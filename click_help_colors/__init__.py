import click
from click.termui import _ansi_colors, _ansi_reset_all


def _colorize(text, color):
    return '\033[%dm' % (_ansi_colors.index(color) + 30) + text + _ansi_reset_all


class HelpColorsFormatter(click.HelpFormatter):
    def write_usage(self, prog, args='', prefix='Usage: '):
        super(HelpColorsFormatter, self).write_usage(prog, args, prefix=_colorize(prefix, color='yellow'))

    def write_heading(self, heading):
        heading = '\033[%dm' % (_ansi_colors.index('yellow') + 30) + heading + ':' + _ansi_reset_all
        self.write('%*s%s\n' % (self.current_indent, '', heading))

    def write_dl(self, *args, **kwargs):
        """Writes a definition list into the buffer.  This is how options
        and commands are usually formatted.

        :param rows: a list of two item tuples for the terms and values.
        :param col_max: the maximum width of the first column.
        :param col_spacing: the number of spaces between the first and
                            second column.
        """
        print args
        super(HelpColorsFormatter, self).write_dl(*args, **kwargs)


class HelpColorsMixin(object):
    def get_help(self, ctx):
        formatter = HelpColorsFormatter(width=ctx.terminal_width,
                                        max_width=ctx.max_content_width)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip('\n')


class HelpColorsGroup(HelpColorsMixin, click.Group):
    def __init__(self, *args, **kwargs):
        super(HelpColorsGroup, self).__init__(*args, **kwargs)


class HelpColorsCommand(HelpColorsMixin, click.Command):
    def __init__(self, *args, **kwargs):
        super(HelpColorsCommand, self).__init__(*args, **kwargs)

    # def get_help_option(self, ctx):
    #     help_options = self.get_help_option_names(ctx)
    #     if not help_options or not self.add_help_option:
    #         return
    #
    #     def show_help(ctx, param, value):
    #         if value and not ctx.resilient_parsing:
    #             self.echo_help(ctx)
    #             ctx.exit()
    #     return Option(help_options, is_flag=True,
    #                   is_eager=True, expose_value=False,
    #                   callback=show_help,
    #                   help='Show this message and exit.')


@click.group(cls=HelpColorsGroup)
def cli():
    pass


@cli.command(cls=HelpColorsCommand)
@click.option('-p', '--pppp', help='Number of greetings.')
def initdb():
    click.echo('Initialized the database')


@cli.command()
def dropdb():
    click.echo('Dropped the database')


if __name__ == '__main__':
    cli()





#
# class HelpFormatter(object):
#     """This class helps with formatting text-based help pages.  It's
#     usually just needed for very special internal cases, but it's also
#     exposed so that developers can write their own fancy outputs.
#
#     At present, it always writes into memory.
#
#     :param indent_increment: the additional increment for each level.
#     :param width: the width for the text.  This defaults to the terminal
#                   width clamped to a maximum of 78.
#     """
#
#     def __init__(self, indent_increment=2, width=None, max_width=None):
#         self.indent_increment = indent_increment
#         if max_width is None:
#             max_width = 80
#         if width is None:
#             width = FORCED_WIDTH
#             if width is None:
#                 width = max(min(get_terminal_size()[0], max_width) - 2, 50)
#         self.width = width
#         self.current_indent = 0
#         self.buffer = []
#
#     def write(self, string):
#         """Writes a unicode string into the internal buffer."""
#         self.buffer.append(string)
#
#     def indent(self):
#         """Increases the indentation."""
#         self.current_indent += self.indent_increment
#
#     def dedent(self):
#         """Decreases the indentation."""
#         self.current_indent -= self.indent_increment
#
#     def write_usage(self, prog, args='', prefix='Usage: '):
#         """Writes a usage line into the buffer.
#
#         :param prog: the program name.
#         :param args: whitespace separated list of arguments.
#         :param prefix: the prefix for the first line.
#         """
#         usage_prefix = '%*s%s ' % (self.current_indent, prefix, prog)
#         text_width = self.width - self.current_indent
#
#         if text_width >= (term_len(usage_prefix) + 20):
#             # The arguments will fit to the right of the prefix.
#             indent = ' ' * term_len(usage_prefix)
#             self.write(wrap_text(args, text_width,
#                                  initial_indent=usage_prefix,
#                                  subsequent_indent=indent))
#         else:
#             # The prefix is too long, put the arguments on the next line.
#             self.write(usage_prefix)
#             self.write('\n')
#             indent = ' ' * (max(self.current_indent, term_len(prefix)) + 4)
#             self.write(wrap_text(args, text_width,
#                                  initial_indent=indent,
#                                  subsequent_indent=indent))
#
#         self.write('\n')
#
#     def write_heading(self, heading):
#         """Writes a heading into the buffer."""
#         self.write('%*s%s:\n' % (self.current_indent, '', heading))
#
#     def write_paragraph(self):
#         """Writes a paragraph into the buffer."""
#         if self.buffer:
#             self.write('\n')
#
#     def write_text(self, text):
#         """Writes re-indented text into the buffer.  This rewraps and
#         preserves paragraphs.
#         """
#         text_width = max(self.width - self.current_indent, 11)
#         indent = ' ' * self.current_indent
#         self.write(wrap_text(text, text_width,
#                              initial_indent=indent,
#                              subsequent_indent=indent,
#                              preserve_paragraphs=True))
#         self.write('\n')
#
#     def write_dl(self, rows, col_max=30, col_spacing=2):
#         """Writes a definition list into the buffer.  This is how options
#         and commands are usually formatted.
#
#         :param rows: a list of two item tuples for the terms and values.
#         :param col_max: the maximum width of the first column.
#         :param col_spacing: the number of spaces between the first and
#                             second column.
#         """
#         rows = list(rows)
#         widths = measure_table(rows)
#         if len(widths) != 2:
#             raise TypeError('Expected two columns for definition list')
#
#         first_col = min(widths[0], col_max) + col_spacing
#
#         for first, second in iter_rows(rows, len(widths)):
#             self.write('%*s%s' % (self.current_indent, '', first))
#             if not second:
#                 self.write('\n')
#                 continue
#             if term_len(first) <= first_col - col_spacing:
#                 self.write(' ' * (first_col - term_len(first)))
#             else:
#                 self.write('\n')
#                 self.write(' ' * (first_col + self.current_indent))
#
#             text_width = max(self.width - first_col - 2, 10)
#             lines = iter(wrap_text(second, text_width).splitlines())
#             if lines:
#                 self.write(next(lines) + '\n')
#                 for line in lines:
#                     self.write('%*s%s\n' % (
#                         first_col + self.current_indent, '', line))
#             else:
#                 self.write('\n')
#
#     @contextmanager
#     def section(self, name):
#         """Helpful context manager that writes a paragraph, a heading,
#         and the indents.
#
#         :param name: the section name that is written as heading.
#         """
#         self.write_paragraph()
#         self.write_heading(name)
#         self.indent()
#         try:
#             yield
#         finally:
#             self.dedent()
#
#     @contextmanager
#     def indentation(self):
#         """A context manager that increases the indentation."""
#         self.indent()
#         try:
#             yield
#         finally:
#             self.dedent()
#
#     def getvalue(self):
#         """Returns the buffer contents."""
#         return ''.join(self.buffer)
