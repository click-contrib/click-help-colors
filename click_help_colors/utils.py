import os

from click.termui import _ansi_colors, _ansi_reset_all


class HelpColorsException(Exception):
    pass


def _colorize(text, color=None):
    if not color or "NO_COLOR" in os.environ:
        return text
    try:
        return '\033[%dm' % (_ansi_colors[color]) + text + _ansi_reset_all
    except KeyError:
        raise HelpColorsException('Unknown color %r' % color)


def _extend_instance(obj, cls):
    """Apply mixin to a class instance after creation"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (cls, base_cls), {})
