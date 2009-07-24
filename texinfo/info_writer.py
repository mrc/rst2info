from docutils import writers
import info_translator

class InfoWriter(writers.Writer):
    supported = ('texinfo')

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = info_translator.InfoTranslator

    def translate(self):
        # print "translate:%s" % self.document.asdom().childNodes[0].toprettyxml('    ','\n')
        self.visitor = visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = self.visitor.astext()
