import textwrap

# utility functions


def get(name):
    direct_lookup = globals().get(f"_help_{name}", None)
    if direct_lookup is not None:
        return direct_lookup

    return _symbol_lookup.get(name, None)


def external(name=None, description=None, url=None, install_url=None):
    def _external_help():
        out = [description.strip()]
        if url is not None:
            out.append(f"For information about {name}, see:\n    {url}")
        try:
            __import__(name)
        except ImportError:
            if install_url is not None:
                out.append(
                    textwrap.dedent(f"""\
                    You do not currently have {name} installed for this version of Python.
                    For information about installing {name}, see:
                        {install_url}
                """)
                )
        return "\n\n".join(s.strip() for s in out if s is not None)

    return _external_help


# specific help functions
# def help_MY_TOPIC() -> str:
#   ...


# a place to add symbols that can't be represented by filenames
# _symbol_lookup['MY_TOPIC'] = lambda() ->str: ...
_symbol_lookup = {}


# auto-generated help functions
