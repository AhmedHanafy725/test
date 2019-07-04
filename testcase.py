from unittest import TestCase
import unittest


class Tests(TestCase):
    def test01_passing(self):
        x = 1
        y = 1
        self.assertEquals(x, y)

    def test02_fail(self):
        x = 1
        y = 2
        self.assertEquals(x, y)

    @unittest.skip("skip test for test")
    def test03_skip(self):
        x = 1

    def test04_error(self):
        x = 1
        y = 0
        z = x / y
        self.assertEquals(x, y)
