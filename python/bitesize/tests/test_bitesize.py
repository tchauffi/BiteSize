import unittest
from bitesize import __author__, __version__


class TestBiteSizeModule(unittest.TestCase):

    def test_author(self):
        self.assertEqual(__author__, "Thibaut Chauffier")

    def test_version(self):
        self.assertEqual(__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
