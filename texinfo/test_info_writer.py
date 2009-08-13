import unittest
from info_writer import InfoWriter

class T(unittest.TestCase):

    def given_input(self, input):
        from docutils.core import publish_string
        settings_overrides={} #{'debug': True}
        self.output = publish_string(input, writer_name='texinfo', settings_overrides=settings_overrides)

    def setUp(self):
        self.writer = InfoWriter()

    def test_writer_supports_texinfo(self):
        self.assertTrue(self.writer.supports('texinfo'))

    def test_translate_alice(self):
        self.given_input("""
********************************
Alice In Wonderland
********************************

================================
Foo
================================

CHAPTER I. Down the Rabbit-Hole
===============================

Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped into the
book her sister was reading, but it had no pictures or conversations in
it, 'and what is the use of a book,' thought Alice 'without pictures or
conversation?'
""")
        self.assertEqual(self.output,
"""\\input texinfo  @c -*-texinfo-*-

@node Top
@top Alice In Wonderland
@majorheading Foo
@chapter CHAPTER I. Down the Rabbit-Hole
Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped into the
book her sister was reading, but it had no pictures or conversations in
it, 'and what is the use of a book,' thought Alice 'without pictures or
conversation?'

""")

    def test_translate_frisbeetarianism(self):
        self.given_input("""
================
Frisbeetarianism
================

Frisbeetarianism is the belief that, when you die, your soul goes up
onto the roof and gets stuck.

Keep in mind always the four constant Laws of Frisbee:

        (1) The most powerful force in the world is that of a disc
            straining to land under a car, just out of reach (this
            force is technically termed "car suck").
        (2) Never precede any maneuver by a comment more predictive
            than "Watch this!"
        (3) The probability of a Frisbee hitting something is directly
            proportional to the cost of hitting it.  For instance, a
            Frisbee will always head directly towards a policeman or
            a little old lady rather than the beat up Chevy.
        (4) Your best throw happens when no one is watching; when the
            cute girl you've been trying to impress is watching, the
            Frisbee will invariably bounce out of your hand or hit you
            in the head and knock you silly.

""")
        self.assertEqual(self.output,
"""\\input texinfo  @c -*-texinfo-*-

@node Top
@top Frisbeetarianism
Frisbeetarianism is the belief that, when you die, your soul goes up
onto the roof and gets stuck.

Keep in mind always the four constant Laws of Frisbee:

@quotation
@enumerate 1
@item
The most powerful force in the world is that of a disc
straining to land under a car, just out of reach (this
force is technically termed "car suck").

@item
Never precede any maneuver by a comment more predictive
than "Watch this!"

@item
The probability of a Frisbee hitting something is directly
proportional to the cost of hitting it.  For instance, a
Frisbee will always head directly towards a policeman or
a little old lady rather than the beat up Chevy.

@item
Your best throw happens when no one is watching; when the
cute girl you've been trying to impress is watching, the
Frisbee will invariably bounce out of your hand or hit you
in the head and knock you silly.

@end enumerate

@end quotation

""")

if __name__=='__main__':
    import unittest
    unittest.main()
