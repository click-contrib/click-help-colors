import sys
import re

from click import echo
from click.decorators import option
from click._compat import iteritems

from .utils import _colorize


def version_option(version=None, *param_decls, **attrs):
    """Adds a ``--version`` option which immediately ends the program
    printing out the version number.  This is implemented as an eager
    option that prints the version and exits the program in the callback.

    :param version: the version number to show.  If not provided Click
                    attempts an auto discovery via setuptools.
    :param prog_name: the name of the program (defaults to autodetection)
    :param message: custom message to show instead of the default
                    (``'%(prog)s, version %(version)s'``)
    :param prog_name_color: color of the prog_name
    :param version_color: color of the version
    :param message_color: default color of the message
    :param others: everything else is forwarded to :func:`option`.
    """
    if version is None:
        if hasattr(sys, '_getframe'):
            module = sys._getframe(1).f_globals.get('__name__')
        else:
            module = ''

    def decorator(f):
        prog_name = attrs.pop('prog_name', None)
        message = attrs.pop('message', '%(prog)s, version %(version)s')
        message_color = attrs.pop('message_color', None)
        prog_name_color = attrs.pop('prog_name_color', message_color)
        version_color = attrs.pop('version_color', message_color)

        def callback(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return
            prog = prog_name
            if prog is None:
                prog = ctx.find_root().info_name
            ver = version
            if ver is None:
                try:
                    import pkg_resources
                except ImportError:
                    pass
                else:
                    for dist in pkg_resources.working_set:
                        scripts = dist.get_entry_map().get('console_scripts') or {}
                        for script_name, entry_point in iteritems(scripts):
                            if entry_point.module_name == module:
                                ver = dist.version
                                break
                if ver is None:
                    raise RuntimeError('Could not determine version')

            msg_parts = []
            for s in re.split(r'(%\(version\)s|%\(prog\)s)', message):
                if s == '%(prog)s':
                    msg_parts.append(_colorize(prog_name, prog_name_color))
                elif s == '%(version)s':
                    msg_parts.append(_colorize(version, version_color))
                else:
                    msg_parts.append(_colorize(s, message_color))

            echo(''.join(msg_parts))
            ctx.exit()

        attrs.setdefault('is_flag', True)
        attrs.setdefault('expose_value', False)
        attrs.setdefault('is_eager', True)
        attrs.setdefault('help', 'Show the version and exit.')
        attrs['callback'] = callback
        return option(*(param_decls or ('--version',)), **attrs)(f)
    return decorator
