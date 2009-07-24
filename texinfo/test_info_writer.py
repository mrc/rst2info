import rst_test_utils
from info_writer import InfoWriter

class T(rst_test_utils.TestCase):

    def given_input(self, input):
        super(T, self).given_input(input)
        self.writer.document = self.document

    def translate(self):
        self.writer.translate()
        self.output = self.writer.output

    def setUp(self):
        self.writer = InfoWriter()

    def test_writer_supports_texinfo(self):
        self.assertTrue(self.writer.supports('texinfo'))

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
        self.translate()
        self.assertEqual(self.output,
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
        
    def test_translate2(self):
        self.given_input("""
================
Frisbeetarianism
================

Frisbeetarianism is the belief that, when you die, your soul goes up
onto the roof and gets stuck.

  Never precede any action with the words "Watch this!"
  -- the first constant Law of Frisbee
""")
        self.translate()
        self.assertEqual(self.output, 
"""\\input texinfo  @c -*-texinfo-*-

@node Top
@top Frisbeetarianism
Frisbeetarianism is the belief that, when you die, your soul goes up
onto the roof and gets stuck.
@quotation
Never precede any action with the words "Watch this!"
-- the first constant Law of Frisbee
@end quotation
""")

if __name__=='__main__':
    import unittest
    unittest.main()
