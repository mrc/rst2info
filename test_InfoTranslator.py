import unittest
from InfoTranslator import InfoTranslator
from docutils import utils

def basic_test_document(text=''):
    t = '''
        
.. hello-world:

****************
Hello, world!
****************
        '''
    from docutils.parsers import rst
    from docutils import frontend
    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    document = utils.new_document('sample', settings)
    parser = rst.Parser()
    parser.parse(text, document)
    return document

class T(unittest.TestCase):

    def setUp(self):
        self.given_input('')

    def given_input(self, input):
        self.document = basic_test_document(input)
        self.visitor = InfoTranslator(self.document)
        self.document.walkabout(self.visitor)

    def test_adds_info_header(self):
        self.assertTrue(self.visitor.astext().startswith('\\input texinfo'))

    def test_doc_has_title(self):
        self.given_input(
'''
****************
Hello, world!
****************
''')
        self.assertEqual(['@node Hello, world!'], self.visitor.body)

    def test_comments_are_comments(self):
        self.given_input(
            '''
.. hello-world:
''')
        self.assertEqual(['@c hello-world:'], self.visitor.body)

    def test_paragraph_text_is_normal_text(self):
        self.given_input(
            """
Someone left the cake out in the rain.
I don't think that I can take it.
            """)
        self.assertEqual(["Someone left the cake out in the rain.\nI don't think that I can take it."], self.visitor.body)

    def test_two_paragraphs(self):
        self.given_input(
            """
MacArthur's park is melting in the dark.

Someone left the cake out in the rain.
I don't think that I can take it.
            """)
        self.assertEqual(["MacArthur's park is melting in the dark.",
                          "Someone left the cake out in the rain.\nI don't think that I can take it."], self.visitor.body)

#    def test_bullets_are_bullets(self):
    
#    def test_dom(self):
#        self.assertEqual(self.document.asdom().toxml(), '???')
