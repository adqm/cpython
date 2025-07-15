import inspect
import doctest
import unittest
import functools

class TestFunctoolsDocTests(unittest.TestCase):
    def test_cache(self):
        @functools.cache
        def foo(x):
            """
            >>> foo(42)
            42
            """
            return x

        def bar(x):
            """
            >>> bar(8)
            8
            """
            return x
        bar = functools.cache(bar)

        def baz(x):
            """
            >>> qux(0)
            0
            """
            return x
        qux = functools.cache(baz)

        tests = doctest.DocTestFinder().find(TestFunctoolsDocTests.test_cache)
        funcs = [bar, baz, foo]
        self.assertEqual(len(tests), 3)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, inspect.cleandoc(func.__doc__))

    def test_cached_property(self):
        class Foo:
            @functools.cached_property
            def bar(self, x):
                """
                >>> f = Foo()
                >>> f.bar(42)
                42
                """
                return x

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.bar]
        self.assertEqual(len(tests), 1)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)

    def test_lru_cache(self):
        @functools.lru_cache
        def foo(x):
            """
            >>> foo(42)
            42
            """
            return x

        def bar(x):
            """
            >>> bar(8)
            8
            """
            return x
        bar = functools.lru_cache(bar)

        def baz(x):
            """
            >>> qux(0)
            0
            """
            return x
        qux = functools.lru_cache(baz)

        tests = doctest.DocTestFinder().find(TestFunctoolsDocTests.test_lru_cache)
        funcs = [bar, baz, foo]
        self.assertEqual(len(tests), 3)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, inspect.cleandoc(func.__doc__))

    def test_singledispatch(self):
        @functools.singledispatch
        def foo(x):
            """
            >>> foo(4.2)
            4.2
            """
            return x

        @foo.register
        def _(x: int):
            """
            >>> foo(4)
            16
            """
            return x**2

        @foo.register
        def _(x: str):
            """
            >>> foo("cat")
            'catcat'
            """
            return x*2

        tests = doctest.DocTestFinder().find(TestFunctoolsDocTests.test_singledispatch)
        print(tests)
        funcs = [foo.registry[k] for k in [object, int, str]]
        self.assertEqual(len(tests), 3)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, inspect.cleandoc(func.__doc__))



if __name__ == "__main__":
    unittest.main(module="test.test_doctest.test_doctest_functools")
