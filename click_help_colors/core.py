import re

import click

from .utils import _colorize, _extend_instance


class HelpColorsFormatter(click.HelpFormatter):
    options_regex = re.compile(r'-{1,2}[\w\-]+')

    def __init__(self, headers_color=None, options_color=None,
                 options_custom_colors=None, *args, **kwargs):
        self.headers_color = headers_color
        self.options_color = options_color
        self.options_custom_colors = options_custom_colors
        super(HelpColorsFormatter, self).__init__(*args, **kwargs)

    def _get_opt_names(self, option_name):
        opts = self.options_regex.findall(option_name)
        if not opts:
            return [option_name]
        else:
            # Include this for backwards compatibility
            opts.append(option_name.split()[0])
            return opts

    def _pick_color(self, option_name):
        opts = self._get_opt_names(option_name)
        for opt in opts:
            if (self.options_custom_colors and
                    (opt in self.options_custom_colors.keys())):
                return self.options_custom_colors[opt]
        return self.options_color

    def write_usage(self, prog, args='', prefix='Usage'):
        colorized_prefix = _colorize(prefix, color=self.headers_color, suffix=": ")
        super(HelpColorsFormatter, self).write_usage(prog,
                                                     args,
                                                     prefix=colorized_prefix)

    def write_heading(self, heading):
        colorized_heading = _colorize(heading, color=self.headers_color)
        super(HelpColorsFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows, **kwargs):
        colorized_rows = [(_colorize(row[0], self._pick_color(row[0])), row[1])
                          for row in rows]
        super(HelpColorsFormatter, self).write_dl(colorized_rows, **kwargs)


class HelpColorsMixin(object):
    def __init__(self, help_headers_color=None, help_options_color=None,
                 help_options_custom_colors=None, *args, **kwargs):
        self.help_headers_color = help_headers_color
        self.help_options_color = help_options_color
        self.help_options_custom_colors = help_options_custom_colors
        super(HelpColorsMixin, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        formatter = HelpColorsFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_color=self.help_headers_color,
            options_color=self.help_options_color,
            options_custom_colors=self.help_options_custom_colors)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip('\n')


class HelpColorsGroup(HelpColorsMixin, click.Group):
    def __init__(self, *args, **kwargs):
        super(HelpColorsGroup, self).__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        kwargs.setdefault('cls', HelpColorsCommand)
        kwargs.setdefault('help_headers_color', self.help_headers_color)
        kwargs.setdefault('help_options_color', self.help_options_color)
        kwargs.setdefault('help_options_custom_colors',
                          self.help_options_custom_colors)
        return super(HelpColorsGroup, self).command(*args, **kwargs)

    def group(self, *args, **kwargs):
        kwargs.setdefault('cls', HelpColorsGroup)
        kwargs.setdefault('help_headers_color', self.help_headers_color)
        kwargs.setdefault('help_options_color', self.help_options_color)
        kwargs.setdefault('help_options_custom_colors',
                          self.help_options_custom_colors)
        return super(HelpColorsGroup, self).group(*args, **kwargs)


class HelpColorsCommand(HelpColorsMixin, click.Command):
    def __init__(self, *args, **kwargs):
        super(HelpColorsCommand, self).__init__(*args, **kwargs)


class HelpColorsMultiCommand(HelpColorsMixin, click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super(HelpColorsMultiCommand, self).__init__(*args, **kwargs)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args[1:] = super(HelpColorsMultiCommand, self).resolve_command(ctx, args)

        if not isinstance(cmd, HelpColorsMixin):
            if isinstance(cmd, click.Group):
                _extend_instance(cmd, HelpColorsGroup)
            if isinstance(cmd, click.Command):
                _extend_instance(cmd, HelpColorsCommand)

        if not getattr(cmd, 'help_headers_color', None):
            cmd.help_headers_color = self.help_headers_color
        if not getattr(cmd, 'help_options_color', None):
            cmd.help_options_color = self.help_options_color
        if not getattr(cmd, 'help_options_custom_colors', None):
            cmd.help_options_custom_colors = self.help_options_custom_colors

        return cmd_name, cmd, args[1:]
