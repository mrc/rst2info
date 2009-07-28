import unittest
from docutils import utils, frontend, core, readers
from docutils.parsers import rst
from info_translator import InfoTranslator

def basic_test_document(text=''):
    reader_name = 'standalone'
    parser_name = 'restructuredtext'

    reader_class = readers.get_reader_class(reader_name)
    reader = reader_class(parser_name=parser_name)
    parser = reader.parser

    options = frontend.OptionParser(components=(parser,reader))
    settings = options.get_default_values()
    document = utils.new_document('rst_test_utils', settings)

    parser.parse(text, document)

    #print 'parser.parse(), document=\n%s' % document.asdom().childNodes[0].toprettyxml('    ','\n')
    return document

class TestCase(unittest.TestCase):
    def given_input(self, input):
        self.document = basic_test_document(input)

