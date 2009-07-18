import unittest
from docutils import utils
from info_translator import InfoTranslator

def basic_test_document(text=''):
    from docutils.parsers import rst
    from docutils import frontend
    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    document = utils.new_document('sample', settings)
    parser = rst.Parser()
    parser.parse(text, document)
    return document

class TestCase(unittest.TestCase):
    def given_input(self, input):
        self.document = basic_test_document(input)

