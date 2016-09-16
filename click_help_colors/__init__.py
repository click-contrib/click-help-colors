import click
from click.termui import _ansi_colors, _ansi_reset_all


def _colorize(text, color=None):
    if not color:
        return text
    try:
        return '\033[%dm' % (_ansi_colors.index(color) + 30) + text + _ansi_reset_all
    except ValueError:
        raise TypeError('Unknown color %r' % color)


class HelpColorsFormatter(click.HelpFormatter):
    def __init__(self, headers_color=None, options_color=None, *args, **kwargs):
        self.headers_color = headers_color
        self.options_color = options_color
        super(HelpColorsFormatter, self).__init__(*args, **kwargs)

    def write_usage(self, prog, args='', prefix='Usage: '):
        colorized_prefix = _colorize(prefix, color=self.headers_color)
        super(HelpColorsFormatter, self).write_usage(prog, args, prefix=colorized_prefix)

    def write_heading(self, heading):
        colorized_heading = _colorize(heading, color=self.headers_color)
        super(HelpColorsFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows, **kwargs):
        colorized_rows = [(_colorize(row[0], self.options_color), row[1]) for row in rows]
        super(HelpColorsFormatter, self).write_dl(colorized_rows, **kwargs)


class HelpColorsMixin(object):
    def __init__(self, help_headers_color=None, help_options_color=None,
                 *args, **kwargs):
        self.help_headers_color = help_headers_color
        self.help_options_color = help_options_color
        super(HelpColorsMixin, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        formatter = HelpColorsFormatter(width=ctx.terminal_width,
                                        max_width=ctx.max_content_width,
                                        headers_color=self.help_headers_color,
                                        options_color=self.help_options_color)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip('\n')


class HelpColorsGroup(HelpColorsMixin, click.Group):
    def __init__(self, *args, **kwargs):
        super(HelpColorsGroup, self).__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        kwargs.setdefault('cls', HelpColorsCommand)
        kwargs.setdefault('help_headers_color', self.help_headers_color)
        kwargs.setdefault('help_options_color', self.help_options_color)
        return super(HelpColorsGroup, self).command(*args, **kwargs)

    def group(self, *args, **kwargs):
        kwargs.setdefault('cls', HelpColorsGroup)
        kwargs.setdefault('help_headers_color', self.help_headers_color)
        kwargs.setdefault('help_options_color', self.help_options_color)
        return super(HelpColorsGroup, self).group(*args, **kwargs)


class HelpColorsCommand(HelpColorsMixin, click.Command):
    def __init__(self, *args, **kwargs):
        super(HelpColorsCommand, self).__init__(*args, **kwargs)
