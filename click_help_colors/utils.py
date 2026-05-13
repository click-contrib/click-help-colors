import os
import typing as t

import click
from click._compat import get_text_stderr
from click.termui import _ansi_colors, _ansi_reset_all


class HelpColorsException(Exception):
    pass


def _colorize(text: str, color: t.Optional[str] = None, suffix: t.Optional[str] = None) -> str:
    if not color or os.getenv("NO_COLOR"):
        return text + (suffix or '')
    try:
        return '\033[%dm' % (_ansi_colors[color]) + text + _ansi_reset_all + (suffix or '')
    except KeyError:
        raise HelpColorsException('Unknown color %r' % color)


def _extend_instance(obj: object, cls: t.Type[object]) -> None:
    """Apply mixin to a class instance after creation"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (cls, base_cls), {})


def _colorize_usage_error(exc: click.UsageError, color: str) -> None:
    """Replace the exception's show() with one that colorizes the ``Error:`` prefix."""
    def show(file: t.Optional[t.IO[t.Any]] = None) -> None:
        if file is None:
            file = get_text_stderr()
        ctx = exc.ctx
        hint = ""
        if ctx is not None and ctx.command.get_help_option(ctx) is not None:
            hint = "Try '{} {}' for help.\n".format(
                ctx.command_path, ctx.help_option_names[0]
            )
        ctx_color = ctx.color if ctx is not None else None
        if ctx is not None:
            click.echo("{}\n{}".format(ctx.get_usage(), hint), file=file, color=ctx_color)
        prefix = _colorize("Error", color=color, suffix=": ")
        click.echo("{}{}".format(prefix, exc.format_message()), file=file, color=ctx_color)

    exc.show = show  # type: ignore[method-assign]
