import rst_test_utils
from info_translator import InfoTranslator

class T(rst_test_utils.TestCase):

    def given_input(self, input):
        super(T, self).given_input(input)
        self.visitor = InfoTranslator(self.document)
        self.document.walkabout(self.visitor)

    def setUp(self):
        self.given_input('')

    def notest_adds_info_header(self):
        self.assertTrue(self.visitor.astext().startswith('\\input texinfo'))

    def test_title(self):
        self.given_input('''
Hello, world!
================
''')
        self.assertEqual(['@node Top', '@top Hello, world!'], self.visitor.body)

    def test_chapter(self):
        self.given_input('''
======
Title!
======

Chapter 1
=========
''')
        self.assertEqual(['@node Top', '@top Title!', '@chapter Chapter 1'],
                         self.visitor.body)

    def test_section(self):
        self.given_input('''
======
Title!
======

Chapter 1
=========

Section 1
---------
''')
        self.assertEqual(['@node Top', '@top Title!',
                          '@chapter Chapter 1',
                          '@section Section 1'],
                         self.visitor.body)

    def test_subsection(self):
        self.given_input('''
======
Title!
======

Chapter 1
=========

Section 1
---------

Subsection 1
~~~~~~~~~~~~
''')
        self.assertEqual(['@node Top', '@top Title!',
                          '@chapter Chapter 1',
                          '@section Section 1',
                          '@subsection Subsection 1'],
                         self.visitor.body)

    def test_section_layering(self):
        self.given_input("""
===================
A Plan for the Moon
===================

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
        self.assertEqual(['@node Top', '@top A Plan for the Moon',
                          '@chapter The Problem',
                          '@section Cheese',
                          '@subsection Lunar mold',
                          '@section Cows',
                          '@chapter A Modest Solution'],
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
        self.assertEqual(["Someone left the cake out in the rain.\nI don't think that I can take it."], self.visitor.body)

    def test_two_paragraphs(self):
        self.given_input("""
MacArthur's park is melting in the dark.

Someone left the cake out in the rain.
I don't think that I can take it.
""")
        self.assertEqual(["MacArthur's park is melting in the dark.",
                          "Someone left the cake out in the rain.\nI don't think that I can take it."], self.visitor.body)


    def test_single_bullet_list(self):
        self.given_input("""
* milk
""")
        self.assertEqual(["@itemize @bullet",
                          "@item",
                          "milk",
                          "",
                          "@end @itemize"], self.visitor.body)

    def test_three_bullet_list(self):
        self.given_input("""
* milk
* eggs
* bread
""")
        self.assertEqual(["@itemize @bullet",
                          "@item",
                          "milk",
                          "",
                          "@item",
                          "eggs",
                          "",
                          "@item",
                          "bread",
                          "",
                          "@end @itemize"], self.visitor.body)

    def notest_indented_block(self):
        self.given_input("""
left aligned.

  indented with two spaces

    indented with four spaces

""")
        self.assertEqual("foo", self.visitor.body)

    def test_literal_block(self):
        self.given_input("""
THE LANDING::

     "Just the place for a Snark!" the Bellman cried,
          As he landed his crew with care;
     Supporting each man on the top of the tide
          By a finger entwined in his hair.

""")
        self.assertEqual(["THE LANDING:",
""""Just the place for a Snark!" the Bellman cried,
     As he landed his crew with care;
Supporting each man on the top of the tide
     By a finger entwined in his hair."""
                          ], self.visitor.body)
