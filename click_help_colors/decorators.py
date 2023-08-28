import re
import typing as t

from .utils import _colorize


from click import version_option as click_version_option, Command

FC = t.TypeVar("FC", bound=t.Union[t.Callable[..., t.Any], Command])


@t.overload
def version_option(
        version: str,
        prog_name: str,
        message: None = ...,
        message_color: t.Optional[str] = ...,
        prog_name_color: t.Optional[str] = ...,
        version_color: t.Optional[str] = ...,
        **kwargs: t.Any,
) -> t.Callable[[FC], FC]: ...


@t.overload
def version_option(
        version: t.Optional[str] = ...,
        prog_name: t.Optional[str] = ...,
        message: str = ...,
        message_color: t.Optional[str] = ...,
        prog_name_color: t.Optional[str] = ...,
        version_color: t.Optional[str] = ...,
        **kwargs: t.Any,
) -> t.Callable[[FC], FC]: ...


def version_option(
        version: t.Optional[str] = None,
        prog_name: t.Optional[str] = None,
        message: t.Optional[str] = None,
        message_color: t.Optional[str] = None,
        prog_name_color: t.Optional[str] = None,
        version_color: t.Optional[str] = None,
        **kwargs: t.Any,
) -> t.Callable[[FC], FC]:
    """
    :param prog_name_color: color of the prog_name.
    :param version_color: color of the version.
    :param message_color: default color of the message.

    for other params see Click's version_option decorator:
    https://click.palletsprojects.com/en/7.x/api/#click.version_option
    """
    if message is None:
        message = "%(prog)s, version %(version)s"

    msg_parts = []
    for s in re.split(r'(%\(version\)s|%\(prog\)s)', message):
        if s == '%(prog)s':
            if prog_name is None:
                raise TypeError("version_option() missing required argument: 'prog_name'")
            msg_parts.append(_colorize(prog_name, prog_name_color or message_color))
        elif s == '%(version)s':
            if version is None:
                raise TypeError("version_option() missing required argument: 'version'")
            msg_parts.append(_colorize(version, version_color or message_color))
        else:
            msg_parts.append(_colorize(s, message_color))
    message = ''.join(msg_parts)

    return click_version_option(
        version=version,
        prog_name=prog_name,
        message=message,
        **kwargs
    )
