def get(name):
    direct_lookup = globals().get(f"_help_{name}", None)
    if direct_lookup is not None:
        return direct_lookup

    return _symbol_lookup.get(name, lambda: "")


# functions for programmatically-generated help text

import io
import random


def _help_pip():
    out = io.StringIO()
    print(
        """\
pip is the package installer for Python. You can use it to install packages
from the Python Package Index and other indexes.

For information about using pip, see:
    https://pip.pypa.io/en/stable/getting-started/
""".rstrip(),
        file=out,
    )

    try:
        import pip
    except ImportError:
        print(
            """

It does not appear that you have pip available.  For information about
installing pip, see:
    https://pip.pypa.io/en/stable/installation/
""".rstrip(),
            file=out,
        )

    return out.getvalue()


# lookup table for symbols that can't be listed as names
_symbol_lookup = {}
