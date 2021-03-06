
import rst_test_utils
from info_translator import InfoTranslator
from docutils.transforms import frontmatter

def strip_comments(body):
    return filter(lambda x: not x.startswith('@c '), body)

class T(rst_test_utils.TestCase):

    def given_input(self, input, transforms=[], settings_overrides={}):
        super(T, self).given_input(input, settings_overrides)
        self.visitor = InfoTranslator(self.document)

        for t in transforms:
            self.document.transformer.add_transform(t)
        self.document.transformer.apply_transforms()

        self.document.walkabout(self.visitor)

    def test_strip_comments(self):
        self.visitor.body = ['Hello', '@c blah', 'World!']
        self.assertEqual(['Hello', '@c blah', 'World!'], self.visitor.body)
        self.assertEqual(['Hello', 'World!'], strip_comments(self.visitor.body))

    def setUp(self):
        self.given_input('')

    def test_adds_info_header(self):
        self.assertTrue(self.visitor.astext().startswith('\\input texinfo'))

    def test_title(self):
        self.given_input('''
Hello, world!
================
''', transforms = [frontmatter.DocTitle])
        self.assertEqual(['@node Top', '@top Hello, world!'], self.visitor.body)

    def test_subtitle(self):
        self.given_input('''
======
Title!
======

--------
Subtitle
--------
''', transforms = [frontmatter.DocTitle])
        self.assertEqual(['@node Top', '@top Title!',
                          '@majorheading Subtitle'],
                         self.visitor.body)

    def test_subsection(self):
        self.given_input('''
Chapter 1
=========

Section 1
---------

Subsection 1
~~~~~~~~~~~~
''')
        self.assertEqual(['@chapter Chapter 1',
                          '@section Section 1',
                          '@subsection Subsection 1'],
                         self.visitor.body)

    def test_section_layering(self):
        self.given_input("""
The Problem
===========

Cheese
------

Lunar mold
~~~~~~~~~~

Cows
----

A Modest Solution
=================
""")
        self.assertEqual(['@chapter The Problem',
                          '@section Cheese',
                          '@subsection Lunar mold',
                          '@section Cows',
                          '@chapter A Modest Solution'],
                         self.visitor.body)

    def test_beyond_subsections(self):
        self.given_input('''
Chapter 1
=========

Section 1
---------

Subsection 1
~~~~~~~~~~~~

Something else
^^^^^^^^^^^^^^

Subsection 2
~~~~~~~~~~~~

Section 2
---------

''')
        self.assertEqual(['@chapter Chapter 1',
                          '@section Section 1',
                          '@subsection Subsection 1',
                          '@subsection Something else',
                          '@subsection Subsection 2',
                          '@section Section 2'],
                         self.visitor.body)

    def test_comments_are_comments(self):
        self.given_input("""
.. hello-world:
""")
        self.assertEqual(['@c hello-world:'], self.visitor.body)

    def test_paragraph_text_is_normal_text(self):
        self.given_input("""
Someone left the cake out in the rain.
I don't think that I can take it.
            """)
        self.assertEqual(["Someone left the cake out in the rain.\nI don't think that I can take it.", ''], self.visitor.body)

    def test_two_paragraphs(self):
        self.given_input("""
MacArthur's park is melting in the dark.

Someone left the cake out in the rain.
I don't think that I can take it.
""")
        self.assertEqual(["MacArthur's park is melting in the dark.", '',
                          "Someone left the cake out in the rain.\nI don't think that I can take it.", ''], self.visitor.body)


    def test_single_bullet_list(self):
        self.given_input("""
* milk
""")
        self.assertEqual(["@itemize @bullet",
                          "@item", "milk", "",
                          "@end @itemize", ""], self.visitor.body)

    def test_three_bullet_list(self):
        self.given_input("""
* milk
* eggs
* bread
""")
        self.assertEqual(["@itemize @bullet",
                          "@item", "milk", "",
                          "@item", "eggs", "",
                          "@item", "bread", "",
                          "@end @itemize", ""], self.visitor.body)

    def test_single_enumerated_list(self):
        self.given_input("""
(1) I was transferred to the moon.
""")
        self.assertEqual(["@enumerate 1",
                          "@item", "I was transferred to the moon.", "",
                          "@end enumerate", ""], self.visitor.body)

    def test_three_item_enumerated_list(self):
        self.given_input("""
(1) I was transferred to the moon.
(2) Worse pay, better hours.
(3) Worse pay, better fellow workers.
""")
        self.assertEqual(["@enumerate 1",
                          "@item", "I was transferred to the moon.", "",
                          "@item", "Worse pay, better hours.", "",
                          "@item", "Worse pay, better fellow workers.", "",
                          "@end enumerate", ""], self.visitor.body)

    def test_single_enumerated_sub_list(self):
        self.given_input("""
a. lower-case letters

   1. with a sub-list
   2. with two items
""")
        self.assertEqual(["@enumerate a",
                          "@item", "lower-case letters", "",
                          "@enumerate 1",
                          "@item", "with a sub-list", "",
                          "@item", "with two items", "",
                          "@end enumerate", "",
                          "@end enumerate", ""], self.visitor.body)

    def test_sub_lists_from_rst_quickstart(self):
        self.given_input("""
1. numbers

A. upper-case letters
   and it goes over many lines

   with two paragraphs and all!

a. lower-case letters

   3. with a sub-list starting at a different number
   4. make sure the numbers are in the correct sequence though!

I. upper-case roman numerals

i. lower-case roman numerals

(1) numbers again

1) and again
""")
        self.assertEqual(["@enumerate 1",
                          "@item", "numbers", "",
                          "@end enumerate", "",

                          "@enumerate A",
                          "@item", "upper-case letters\nand it goes over many lines", "",
                          "with two paragraphs and all!", "",
                          "@end enumerate", "",

                          "@enumerate a",
                          "@item", "lower-case letters", "",
                          "@enumerate 3",
                          "@item", "with a sub-list starting at a different number", "",
                          "@item", "make sure the numbers are in the correct sequence though!", "",
                          "@end enumerate", "",
                          "@end enumerate", "",

                          "@enumerate 1",
                          "@item", "upper-case roman numerals", "",
                          "@end enumerate", "",

                          "@enumerate 1",
                          "@item", "lower-case roman numerals", "",
                          "@end enumerate", "",

                          "@enumerate 1",
                          "@item", "numbers again", "",
                          "@end enumerate", "",

                          "@enumerate 1",
                          "@item", "and again", "",
                          "@end enumerate", ""], strip_comments(self.visitor.body))

    def test_system_message(self):
        self.given_input("""
3. Lists generally don't start at 3
""", settings_overrides={'report_level':1})
        self.assertEqual(["@enumerate 3",
                          "@item", "Lists generally don't start at 3", "",
                          "@end enumerate", "",
                          "@c System Message: INFO/1 (rst_test_utils:, line 2)",
                          "@c Enumerated list start value not ordinal-1: \"3\" (ordinal 3)",
                          "@c --end system message--"], self.visitor.body)

    def test_system_message_below_report_level(self):
        self.given_input("""
3. Lists generally don't start at 3
""")
        self.assertEqual(["@enumerate 3",
                          "@item", "Lists generally don't start at 3", "",
                          "@end enumerate", ""
                          ], self.visitor.body)

    def test_quotation(self):
        self.given_input("""
  Never precede any action with the words "Watch this!"
  -- the second constant Law of Frisbee

""")
        self.assertEqual(["@quotation",
'''Never precede any action with the words "Watch this!"
-- the second constant Law of Frisbee''', '',
                          "@end quotation", ""], self.visitor.body)

    def test_formatted_code(self):
        self.given_input("""
Frisbeetarianism is the belief that, when you die, your soul goes up
onto the roof and gets stuck.

  Never precede any action with the words "Watch this!"
  -- the second constant Law of Frisbee
""")
        self.assertEqual([
'''Frisbeetarianism is the belief that, when you die, your soul goes up
onto the roof and gets stuck.''', '',
"@quotation",
'''Never precede any action with the words "Watch this!"
-- the second constant Law of Frisbee''', '',
                          "@end quotation", ""], self.visitor.body)

    def test_literal_block(self):
        self.given_input("""
THE LANDING::

     "Just the place for a Snark!" the Bellman cried,
          As he landed his crew with care;
     Supporting each man on the top of the tide
          By a finger entwined in his hair.

""")
        self.assertEqual(["THE LANDING:", '',
""""Just the place for a Snark!" the Bellman cried,
     As he landed his crew with care;
Supporting each man on the top of the tide
     By a finger entwined in his hair."""], self.visitor.body)

    def test_definition_list(self):
        self.given_input("""
what
  Definition lists associate a term with a definition.

how
  The term is a one-line phrase, and the definition is one or more
  paragraphs or body elements, indented relative to the term.
  Blank lines are not allowed between term and definition.
""")
        self.assertEqual(["what",
                          "@quotation",
                          "Definition lists associate a term with a definition.",
                          "",
                          "@end quotation", "",
                          "how",
                          "@quotation",
                          "The term is a one-line phrase, and the definition is one or more\n"
                          "paragraphs or body elements, indented relative to the term.\n"
                          "Blank lines are not allowed between term and definition.",
                          "",
                          "@end quotation", ""], self.visitor.body)
