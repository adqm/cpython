import doctest
import unittest

class TestNestedPropertyDocTests(unittest.TestCase):
    def test_closures(self):
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

        tests = doctest.DocTestFinder().find(foo)
        self.assertEqual(len(tests), 3)

    def test_class_in_func(self):
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
        tests = doctest.DocTestFinder().find(fooclass)
        self.assertEqual(len(tests), 3)
        for (n, test) in zip([30, 40, 50], tests):
            self.assertIn(str(n), test.docstring)


if __name__ == '__main__':
    unittest.main(module='test.test_doctest.test_doctest_properties')

