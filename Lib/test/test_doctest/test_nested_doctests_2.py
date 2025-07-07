import doctest
import unittest

def foo(x):
    """
    >>> foo(10)(30)(50)
    90
    """
    def bar(y):
        """
        >>> foo(20)(40)(60)
        120
        """
        def baz(z):
            """
            >>> foo(30)(60)(90)
            180
            """
            return y + x + z
        return baz
    return bar

def fooclass(x):
    """
    >>> fooclass(30)().x
    30
    """
    class Foo:
        """
        >>> fooclass(40)().x
        40
        """
        def __init__(self):
            """
            >>> fooclass(50)().x
            50
            """
            self.x = x
    return Foo


def load_tests(loader, tests, pattern):
    tests.addTest(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    unittest.main()
