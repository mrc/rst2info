import rst_test_utils
from info_writer import InfoWriter

class T(rst_test_utils.TestCase):

    def given_input(self, input):
        super(T, self).given_input(input)
        self.writer.document = self.document

    def setUp(self):
        self.writer = InfoWriter()

    def test_writer_supports_info(self):
        self.assertTrue(self.writer.supports('info'))

    def test_translate(self):
        self.given_input("""
********************************
Alice In Wonderland
********************************

CHAPTER I. Down the Rabbit-Hole
===============================

Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped into the
book her sister was reading, but it had no pictures or conversations in
it, 'and what is the use of a book,' thought Alice 'without pictures or
conversation?'
""")
        self.writer.translate()
        self.assertEqual(self.writer.output,
"""\\input texinfo  @c -*-texinfo-*-

@node Top
@top Alice In Wonderland
@chapter CHAPTER I. Down the Rabbit-Hole
Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped into the
book her sister was reading, but it had no pictures or conversations in
it, 'and what is the use of a book,' thought Alice 'without pictures or
conversation?'
""")
        
        
