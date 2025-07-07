import doctest
import unittest

class TestFragileDocTestCases(unittest.TestCase):
    def test_fragile_classdefs(self):
        class A:
            """
            >>> A.x
            20
            """
            x = 20

        class A:
            """
            >>> A.x
            30
            """

        test = doctest.DocTestFinder().find(A)[0]
        self.assertEqual(test.docstring, A.__doc__)
        self.assertEqual(test.lineno, A.__firstlineno__)

    def test_fragile_funcdefs(self):
        def foo(x, y, z=
                "cat"):
            """
            >>> x
            7
            """

        test = doctest.DocTestFinder().find(foo)[0]
        self.assertEqual(test.docstring, foo.__doc__)
        self.assertEqual(test.lineno, foo.__code__.co_firstlineno+1)

