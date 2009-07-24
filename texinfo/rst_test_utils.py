import unittest
from docutils import utils
from info_translator import InfoTranslator

def basic_test_document(text=''):
    from docutils.parsers import rst
    from docutils import frontend

    overrides = {'initial_header_level': 1}
    option_parser = frontend.OptionParser(components=(rst.Parser,), defaults=overrides)
    settings = option_parser.get_default_values()



    document = utils.new_document('rst_test_utils', settings)

    print "translate:%s" % document.asdom().childNodes[0].toprettyxml('    ','\n')

    parser = rst.Parser()
    parser.parse(text, document)

    print "translate:%s" % document.asdom().childNodes[0].toprettyxml('    ','\n')

    return document

class TestCase(unittest.TestCase):
    def given_input(self, input):
        self.document = basic_test_document(input)

