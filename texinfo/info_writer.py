from docutils import writers
import InfoTranslator

class InfoWriter(writers.Writer):
    supported = ('info')

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = InfoTranslator.InfoTranslator

    def translate(self):
        self.visitor = visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = self.visitor.astext()
