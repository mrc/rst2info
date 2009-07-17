import unittest
from InfoWriter import InfoWriter

class T(unittest.TestCase):

    def setUp(self):
        self.w = InfoWriter()

    def test_writer_supports_info(self):
        self.assertTrue(self.w.supports('info'))
