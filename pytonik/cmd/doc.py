# Author : BetaCodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by BetaCodings on 1/19/20.


import argparse
import locale
import os
import re
import sys
import time
import warnings
from pytonik.cmd import lang
from pytonik import Version
from typing import Any, Callable, Dict, List, Pattern, Union
from pytonik.cmd.console import (  # type: ignore
    colorize, bold, red, turquoise, nocolor, color_terminal
)

import webbrowser

from random import randint

try:
    import readline

    if readline.__doc__ and 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
        USE_LIBEDIT = True
    else:
        readline.parse_and_bind("tab: complete")
        USE_LIBEDIT = False
except ImportError:
    USE_LIBEDIT = False



class ValidationError(Exception):
    """Raised for validation errors."""


def is_path(x: str) -> str:
    x = os.path.expanduser(x)
    if not os.path.isdir(x):
        raise ValidationError(__("Please enter a valid path name."))
    return x


def boolean(x: str) -> bool:
    if x.upper() not in ('Y', 'YES', 'N', 'NO'):
        raise ValidationError(__("Please enter either 'y' or 'n'."))
    return x.upper() in ('Y', 'YES')


def allow_empty(x: str) -> str:
    return x


def nonempty(x: str) -> str:
    if not x:
        raise ValidationError(__("Please enter some text."))
    return x


def __(mes_id):

    try:
        userlang = locale.getlocale()[0]

        l_ = mes_id
        for l in lang.lang:
            if l == str(userlang):
                getla = lang.lang.get(l, '')

                if getla != "":
                    l_ =  getla.get(mes_id, '')
                    if l_ != "":
                        l_ = getla.get(mes_id, '')
                    else:
                        l_ = mes_id
                else:
                    l_ = mes_id
    except Exception as arr:
        l_ = mes_id
    return l_

def doTraceBack():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
    traceback.print_exc()



if sys.platform == 'win32':
    # On Windows, show questions as bold because of color scheme of PowerShell (refs: #5294).
    COLOR_QUESTION = 'bold'
else:
    COLOR_QUESTION = 'purple'

PROMPT_PREFIX = '> '


def do_prompt(text: str, default: str = None, validator: Callable[[str], Any] = nonempty) -> Union[str, bool]:  # NOQA

    while True:

        if default is not None:
            prompt = PROMPT_PREFIX + '%s [%s]: ' % (text, default)
        else:
            prompt = PROMPT_PREFIX + text + ': '
        if USE_LIBEDIT:
            # Note: libedit has a problem for combination of ``input()`` and escape
            # sequence (see #5335).  To avoid the problem, all prompts are not colored
            # on libedit.
            pass
        else:
            prompt = colorize(COLOR_QUESTION, prompt, input_mode=True)
        x = term_input(prompt).strip()
        if default and not x:
            x = default
        try:
            x = validator(x)
        except ValidationError as err:
            print(red('* ' + str(err)))
            continue
        break
    return x


def term_input(prompt: str) -> str:
    if sys.platform == 'win32':

        print(prompt, end='')
        return input('')
    else:
        return input(prompt)



def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS] <PROJECT_DIR>',
        epilog=__("For more information, visit < https://pytonik.readthedocs.io >."),
        description=__("""Pytonik is a python framework built to enhance web development
        fast and easy, also help web developers to build more apps with less codes.
        it uses expressive architectural pattern, structured on model view controller MVC
        and bundles of component to reuse while deploying the framework."""))

    parser.add_argument('-q', '--quit', action='store_true', dest='quit',
                        default=None,
                        help=__('quit mode'))
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % Version.VERSION_TEXT)

    parser.add_argument('path', metavar='PROJECT_DIR', default='.', nargs='?',
                        help=__('project root'))

    return parser

def ask(d: Dict) -> None:
    print(bold(__('Run Pytonik Server.')))

    d['run'] = do_prompt(__('Do you want to run this project (y/n)'), 'n', boolean)

    if d.get('run', '') is True:

        serv()

    else:
        sys.exit(-1)

        print()


def main(argv: List[str] = sys.argv[1:]) -> int:
    # parse options
    parser = get_parser()
    try:
        args = parser.parse_args(argv)

    except SystemExit as err:
        return err.code
    d = vars(args)
    import http.server
    import socketserver

    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = 'docs'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Create an object of the above class
    handler_object = MyHttpRequestHandler

    PORT = randint(1000, 9999)
    url = "http://localhost"
    my_server = socketserver.TCPServer(("localhost", PORT), handler_object)

    l = "{}:{}".format(url, PORT)
    webbrowser.open_new(l)
    # Star the server
    my_server.serve_forever()



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))