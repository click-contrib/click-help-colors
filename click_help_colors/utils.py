import os
import typing as t

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
