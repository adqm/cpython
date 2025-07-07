import doctest
import unittest


class TestPropertyDocTests(unittest.TestCase):
    def test_property_decorators(self):
        class Foo:
            @property
            def x(self):
                """
                >>> f = Foo()
                >>> f.x
                42
                """
                return 42

            @x.setter
            def x(self, val):
                """
                >>> f = Foo()
                >>> f.x = 27
                >>> f.y
                27
                """
                self.y = val

            @x.deleter
            def x(self):
                """
                >>> f = Foo()
                >>> del f.x
                DELORTED
                """
                print('DELORTED')

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.x, Foo.x.fdel, Foo.x.fset]
        self.assertEqual(len(tests), 3)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)

    def test_property_decorators_onlydel(self):
        class Foo:
            @property
            def x(self):
                return 42

            @x.setter
            def x(self, val):
                self.y = val

            @x.deleter
            def x(self):
                """
                >>> f = Foo()
                >>> del f.x
                DELORTED
                """
                print('DELORTED')

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.x.fdel]
        self.assertEqual(len(tests), 1)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)

    def test_property_direct_extradocstring(self):
        class Foo:
            def xget(self):
                """
                >>> f = Foo()
                >>> f.x
                42
                """
                return 42

            def xset(self, val):
                """
                >>> f = Foo()
                >>> f.x = 27
                >>> f.y
                27
                """
                self.y = val

            def xdel(self):
                """
                >>> f = Foo()
                >>> del f.x
                DELORTED
                """
                print('DELORTED')

            x = property(xget, xset, xdel, ">>> 'test'\n'test'")

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.x, Foo.xdel, Foo.xget, Foo.xset]
        self.assertEqual(len(tests), 4)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)

    def test_property_direct_noextradocstring(self):
        class Foo:
            def xget(self):
                """
                >>> f = Foo()
                >>> f.x
                42
                """
                return 42

            def xset(self, val):
                """
                >>> f = Foo()
                >>> f.x = 27
                >>> f.y
                27
                """
                self.y = val

            def xdel(self):
                """
                >>> f = Foo()
                >>> del f.x
                DELORTED
                """
                print('DELORTED')

            x = property(xget, xset, xdel)

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.xdel, Foo.xget, Foo.xset]
        self.assertEqual(len(tests), 3)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)

    def test_property_direct_onedocstring(self):
        class Foo:
            def xget(self):
                """
                >>> f = Foo()
                >>> f.x
                42
                """
                return 42

            def xset(self, val):
                self.y = val

            def xdel(self):
                print('DELORTED')

            x = property(xget, xset, xdel)

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.x]
        self.assertEqual(len(tests), 1)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)

    def test_property_direct_onedocstring_extra(self):
        class Foo:
            _doc = """
                >>> f = Foo()
                >>> f.x
                42
                """

            def xget(self):
                return 42

            def xset(self, val):
                self.y = val

            def xdel(self):
                print('DELORTED')

            x = property(xget, xset, xdel, _doc)

        tests = doctest.DocTestFinder().find(Foo)
        funcs = [Foo.x]
        self.assertEqual(len(tests), 1)
        for test, func in zip(tests, funcs):
            self.assertEqual(test.docstring, func.__doc__)


if __name__ == '__main__':
    unittest.main(module='test.test_doctest.test_doctest_properties')
