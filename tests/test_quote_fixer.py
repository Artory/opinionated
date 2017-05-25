from lib2to3.tests.test_fixers import FixerTestCase
import os

path = os.path.dirname(os.path.abspath(__file__))

class MyFTC(FixerTestCase):
    def setUp(self, *args, **kwargs):
        kwargs["fixer_pkg"] = "opinionated"
        super().setUp(*args, **kwargs)

class TestQuotes(MyFTC):
    fixer = "quotes"

    def test_basic(self):
        b = """
        a = b"test"
        """

        a = """
        a = b'test'
        """
        self.check(b, a)

    def test_sample(self):
        a = open(path + '/workdir/sample.py').read()
        b = open(path + '/workdir/sample_single.py').read()
        self.check(a, b)

    def test_config_behavior(self):
        b = """
        a = "test"
        """

        a = """
        a = 'test'
        """
        self.filename = path + '/workdir/outer/somefile.py'
        self.check(b, a)
        self.filename = path + '/workdir/outer/inner/somefile.py'
        self.unchanged(b, b)
