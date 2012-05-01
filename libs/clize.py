from __future__ import print_function
from functools import wraps, partial
from collections import namedtuple
import re
from textwrap import TextWrapper
from traceback import print_exc

import sys
import os
import inspect
from gettext import gettext as _, ngettext as _n

class ArgumentError(TypeError):

    def __str__(self):
        return str(self.args[0] + '\n'
            + help(self.args[2], self.args[1],
                   just_do_usage=True, do_print=False))

Option = namedtuple(
    'Option',
    (
        'source',
        'names',
        'default',
        'type',
        'help',
        'optional',
        'positional',
        'takes_argument',
        'catchall',
        )
    )

def make_flag(
        source,
        names,
        default=False,
        type=bool,
        help='',
        takes_argument=0,
        ):
    return Option(
        source, names, default, type, help,
        optional=True, positional=False,
        takes_argument=takes_argument, catchall=False
        )

Command = namedtuple(
    'Command',
    (
        'description',
        'footnotes',
        'posargs',
        'options'
        )
    )

argdesc = re.compile('^(\w+): (.*)$', re.DOTALL)

def read_arguments(fn, alias, force_positional, require_excess, coerce):
    argspec = inspect.getargspec(fn)

    doc = inspect.getdoc(fn)
    description = []
    footnotes = []
    opts_help = {}

    if doc:
        for paragraph in doc.split('\n\n'):
            m = argdesc.match(paragraph)

            if m:
                optname, desc = m.groups()
                opts_help[optname] = desc
            else:
                if opts_help:
                    footnotes.append(paragraph)
                else:
                    description.append(paragraph)

    posargs = []
    options = []

    for i, argname in enumerate(argspec.args):
        try:
            default = argspec.defaults[-len(argspec.args) + i]
        except (IndexError, TypeError):
            default = None
            optional = False
            type_ = str
        else:
            optional = True
            type_ = type(default)

        type_ = coerce.get(argname, type_)

        positional = not optional
        if argname in force_positional:
            positional = True

        if positional and options and options[-1].optional:
            optional = True

        option = Option(
            source=argname,
            names=(argname.replace('_', '-'),) + alias.get(argname, ()),
            default=default,
            type=type_,
            help=opts_help.get(argname, ''),
            optional=optional,
            positional=positional,
            takes_argument=int(optional and type_ != bool),
            catchall=False,
            )
        if positional:
            posargs.append(option)
        else:
            options.append(option)

    if argspec.varargs:
        posargs.append(
            Option(
                source=argspec.varargs,
                names=(argspec.varargs.replace('_', '-'),),
                default=None,
                type=str,
                help=opts_help.get(argspec.varargs, ''),
                optional=bool(not require_excess or posargs and posargs[-1].optional),
                positional=True,
                takes_argument=False,
                catchall=True,
            )
        )

    return Command(
        description=tuple(description), footnotes=tuple(footnotes),
        posargs=posargs, options=options)

def get_arg_name(arg):
    name = arg.names[0] + (arg.catchall and '...' or '')
    return (arg.optional and '[' + name + ']'
            or name)

def get_option_names(option):
    shorts = []
    longs = []

    for name in option.names:
        if option.positional:
            longs.append(name)
        elif len(name) == 1:
            shorts.append('-' + name)
        else:
            longs.append('--' + name)

    if ((not option.positional and option.type != bool)
            or (option.positional and option.type != str)):
        longs[-1] += '=' + option.type.__name__.upper()

    if option.positional and option.catchall:
        longs[-1] += '...'

    return ', '.join(shorts + longs)

def get_terminal_width():
    return 70 #fair terminal dice roll

def print_arguments(arguments, width=None):
    if width == None:
        width = 0
        for arg in arguments:
            width = max(width, len(get_option_names(arg)))

    help_wrapper = TextWrapper(
        width=get_terminal_width(),
        initial_indent=' ' * (width + 5),
        subsequent_indent=' ' * (width + 5),
        )

    return ('\n'.join(
        ' ' * 2 + '{0:<{width}}  {1}'.format(
            get_option_names(arg),
            arg.help and help_wrapper.fill(
                arg.help +
                    (arg.default not in (None, False)
                        and _('(default: {0!r})').format(arg.default)
                    or '')
            )[width + 4:]
                or '',
            width=width,
        ) for arg in arguments))

def help(name, command, just_do_usage=False, do_print=True, **kwargs):
    ret = ""
    ret += (_('Usage: {0}{1} {2}').format(
        name,
        command.options and _(' [OPTIONS]') or '',
        ' '.join(get_arg_name(arg) for arg in command.posargs),
        ))

    if just_do_usage:
        if do_print:
            print(ret)
        return ret

    tw = TextWrapper(
        width=get_terminal_width()
        )

    ret += '\n\n'.join(
        tw.fill(p) for p in ('',) + command.description) + '\n'
    if command.posargs:
        ret += '\n' + _('Positional arguments:') + '\n'
        ret += print_arguments(command.posargs) + '\n'
    if command.options:
        ret += '\n' + _('Options:') + '\n'
        ret += print_arguments(command.options) + '\n'
    if command.footnotes:
        ret += '\n' + '\n\n'.join(tw.fill(p) for p in command.footnotes)
        ret += '\n'

    if do_print:
        print(ret)

    return ret

def get_option(name, list):
    for option in list:
        if name in option.names:
            return option
    raise KeyError

def coerce_option(val, option, key, command, name):
    try:
        return option.type(val)
    except ValueError:
        key = (len(key) == 1 and '-' + key) or ('--' + key)
        raise ArgumentError(_("{0} needs an argument of type {1}")
            .format(key, option.type.__name__.upper()),
            name, command
            )

def set_arg_value(val, option, key, params, name, command):
    if callable(option.source):
        return option.source(name=name, command=command,
                             val=val, params=params)
    else:
        params[option.source] = coerce_option(
            val, option, key, name, command)

def get_following_arguments(i, option, input, key, command, name):
    if i + option.takes_argument >= len(input):
        raise ArgumentError(
            _n("--{0} needs an argument.",
               "--{0} needs {1} arguments.",
               option.takes_argument)
            .format(key, option.takes_argument),
            command, name
            )

    if option.catchall:
        val_ = input[i+1:]
    else:
        val_ = input[
            i+1:i+option.takes_argument+1]

    return len(val_), ' '.join(val_)

def clize(
        fn=None,
        alias={},
        help_names=('help', 'h'),
        force_positional=(),
        coerce={},
        require_excess=False,
        extra=(),
    ):
    def _wrapperer(fn):
        command = read_arguments(
            fn,
            alias, force_positional,
            require_excess, coerce,
            )

        if help_names:
            help_option = make_flag(
                source=help,
                names=help_names,
                help=_("Show this help"),
                )
            command.options.append(help_option)

        command.options.extend(extra)

        @wraps(fn)
        def _getopts(*input):
            name = input[0]
            input = input[1:]

            kwargs = {}
            args = []

            skip_next = 0
            for i, arg in enumerate(input):
                if skip_next:
                    skip_next -= 1
                    continue

                if arg.startswith('--'):
                    if len(arg) == 2:
                        args.extend(input[i+1:])
                        break

                    keyarg = arg[2:].split('=', 1)
                    try:
                        option = get_option(keyarg[0], command.options)
                    except KeyError:
                        raise ArgumentError(
                            _("Unrecognized option {0}").format(arg),
                            command,
                            name
                            )
                    else:
                        if option.takes_argument or option.catchall:
                            try:
                                key, val = keyarg
                            except ValueError:
                                key = keyarg[0]

                                skip_next, val = get_following_arguments(
                                    i, option, input, key, command, name
                                    )
                        else:
                            key = keyarg[0]
                            val = True
                        if set_arg_value(
                                val, option, key,
                                kwargs,
                                name, command
                                ):
                            return
                elif arg.startswith('-'):
                    skip_next_ = 0
                    for j, c in enumerate(arg[1:]):
                        if skip_next_:
                            skip_next_ -= 1
                            continue

                        try:
                            option = get_option(c, command.options)
                        except KeyError:
                            raise ArgumentError(_("Unknown option -{0}.").format(c),
                                                command, name)
                        else:
                            if option.takes_argument:
                                if len(arg) > 2+j:
                                    if option.type == int:
                                        val = ""
                                        for k in range(2+j, len(arg)):
                                            if k == 2+j and arg[k] == '-':
                                                val += '-'
                                            elif '0' <= arg[k] and arg[k] <= '9':
                                                val += arg[k]
                                            else:
                                                break
                                    else:
                                        val = arg[2+j:]
                                    skip_next_ = len(val)
                                else:
                                    skip_next, val = get_following_arguments(
                                        i, option, input, option.source, command, name
                                        )
                            else:
                                val = True

                            if set_arg_value(
                                    val, option, c,
                                    kwargs,
                                    name, command
                                    ):
                                return
                else:
                    args.append(arg)

            for i, option in enumerate(command.posargs):
                if i >= len(args):
                    if option.optional:
                        if not option.catchall:
                            args.append(option.default)
                    else:
                        raise ArgumentError(_("Not enough arguments."), command, name)
                if not option.catchall:
                    args[i] = option.type(args[i])


            if len(args) != len(command.posargs):
                if (not command.posargs
                   or not command.posargs[-1].catchall):
                    raise ArgumentError(_("Too many arguments."), command, name)

            for option in command.options:
                if not callable(option.source):
                    kwargs.setdefault(option.source, option.default)

            fn_args = inspect.getargspec(fn).args
            for i, key in enumerate(fn_args):
                if key in kwargs:
                    args.insert(i, kwargs[key])

            return fn(*args)
        return _getopts

    if fn == None:
        return _wrapperer
    else:
        return _wrapperer(fn)

def run(fn, args=None):
    if args == None:
        args = sys.argv

    import os.path
    try:
        fn(*sys.argv)
    except ArgumentError as e:
        print(os.path.basename(args[0]) + ': ' + str(e),
              file=sys.stderr)
