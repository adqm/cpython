"""A simple SQLite CLI for the sqlite3 module.

Apart from using 'argparse' for the command-line interface,
this module implements the REPL as a thin wrapper around
the InteractiveConsole class from the 'code' stdlib module.
"""
import sqlite3
import os
import sys

from argparse import ArgumentParser
from cmd import Cmd
from textwrap import dedent
from _colorize import get_theme, theme_no_color

from ._completer import completer


def execute(c, sql, suppress_errors=True, theme=theme_no_color):
    """Helper that wraps execution of SQL code.

    This is used both by the REPL and by direct execution from the CLI.

    'c' may be a cursor or a connection.
    'sql' is the SQL string to execute.
    """

    try:
        for row in c.execute(sql):
            print(row)
    except sqlite3.Error as e:
        t = theme.traceback
        tp = type(e).__name__
        try:
            tp += f" ({e.sqlite_errorname})"
        except AttributeError:
            pass
        print(
            f"{t.type}{tp}{t.reset}: {t.message}{e}{t.reset}", file=sys.stderr
        )
        if not suppress_errors:
            sys.exit(1)


class SqliteInteractiveConsole(Cmd):
    """A simple SQLite REPL."""

    def __init__(self, connection, use_color=False):
        super().__init__(completekey=None)
        self._con = connection
        self._cur = connection.cursor()
        self._use_color = use_color
        theme = get_theme(force_no_color=not self._use_color)
        s = theme.syntax
        self.ps1 = f"{s.prompt}sqlite> {s.reset}"
        self.ps2 = f"{s.prompt}    ... {s.reset}"
        self.reset()

    def reset(self):
        self.buffer = []
        self.prompt = self.ps1

    def run_and_clear_buffer(self):
        try:
            execute(
                self._cur,
                os.linesep.join(self.buffer),
                theme=get_theme(force_no_color=not self._use_color),
            )
        finally:
            self.reset()

    def onecmd(self, source):
        """
        Accept a single line of input.

        Return True if it's time to exit the REPL.
        Return False if we should loop again (either for fresh input or as part
        of a multiline input.
        """
        theme = get_theme(force_no_color=not self._use_color)

        if not source or source.isspace():
            return False

        # Remember to update CLI_COMMANDS in _completer.py
        if source[0] == "." and not self.buffer:
            match source[1:].strip():
                case "version":
                    print(sqlite3.sqlite_version)
                case "help":
                    t = theme.syntax
                    print(f"Enter SQL code or one of the below commands, and press enter.\n\n"
                          f"{t.builtin}.version{t.reset}    Print underlying SQLite library version\n"
                          f"{t.builtin}.help{t.reset}       Print this help message\n"
                          f"{t.builtin}.quit{t.reset}       Exit the CLI, equivalent to CTRL-D\n")
                case "quit":
                    return True
                case "":
                    pass
                case _ as unknown:
                    t = theme.traceback
                    print(f'{t.type}Error{t.reset}: {t.message}unknown '
                          f'command: "{unknown}"{t.reset}\n', file=sys.stderr)
        elif source == "EOF":
            return True
        else:
            self.buffer.append(source)
            if not sqlite3.complete_statement(os.linesep.join(self.buffer)):
                self.prompt = self.ps2
                return False
            self.run_and_clear_buffer()
        return False


def main(*args):
    parser = ArgumentParser(
        description="Python sqlite3 CLI",
        color=True,
    )
    parser.add_argument(
        "filename", type=str, default=":memory:", nargs="?",
        help=(
            "SQLite database to open (defaults to ':memory:'). "
            "A new database is created if the file does not previously exist."
        ),
    )
    parser.add_argument(
        "sql", type=str, nargs="?",
        help=(
            "An SQL query to execute. "
            "Any returned rows are printed to stdout."
        ),
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"SQLite version {sqlite3.sqlite_version}",
        help="Print underlying SQLite library version",
    )
    args = parser.parse_args(*args)

    if args.filename == ":memory:":
        db_name = "a transient in-memory database"
    else:
        db_name = repr(args.filename)

    # Prepare REPL banner and prompts.
    if sys.platform == "win32" and "idlelib.run" not in sys.modules:
        eofkey = "CTRL-Z"
    else:
        eofkey = "CTRL-D"
    banner = dedent(f"""
        sqlite3 shell, running on SQLite version {sqlite3.sqlite_version}
        Connected to {db_name}

        Each command will be run using execute() on the cursor.
        Type ".help" for more information; type ".quit" or {eofkey} to quit.
    """).strip()

    theme = get_theme()
    s = theme.syntax

    sys.ps1 = f"{s.prompt}sqlite> {s.reset}"
    sys.ps2 = f"{s.prompt}    ... {s.reset}"

    con = sqlite3.connect(args.filename, isolation_level=None)
    try:
        if args.sql:
            # SQL statement provided on the command-line; execute it directly.
            execute(con, args.sql, suppress_errors=False, theme=theme)
        else:
            # No SQL provided; start the REPL.
            print(banner, file=sys.stderr)
            with completer():
                console = SqliteInteractiveConsole(con, use_color=True)
                while True:
                    try:
                        console.cmdloop()
                        break
                    except KeyboardInterrupt:
                        print("^C")
                        console.reset()
    finally:
        con.close()

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
