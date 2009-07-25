from docutils import nodes
import exceptions

class InfoTranslator(nodes.NodeVisitor):

    document_start = """\\input texinfo  @c -*-texinfo-*-
"""
    
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        self.header = []
        self.body = []
        self.section_level = 0
        self.docinfo = {}

    def astext(self):
        return '\n'.join(self.header + self.body + [''])

    def visit_document(self, node):
        self.header.append(self.document_start)
    
    def depart_document(self, node):
        pass

    def visit_comment(self, node):
        self.body.append('@c %s' % node.astext())
        raise nodes.SkipNode

    def visit_section(self, node):
        self.section_level += 1
        #self.body.append('@c +s %d' % self.section_level)

    def depart_section(self, node):
        self.section_level -= 1
        #self.body.append('@c -s %d' % self.section_level)

    def emit_title(self, text):
        self.body.append('@node Top')
        self.body.append('@top %s' % text)

    def emit_chapter(self, text):
        self.body.append('@chapter %s' % text)

    def emit_section(self, text):
        self.body.append('@section %s' % text)

    def emit_subsection(self, text):
        self.body.append('@subsection %s' % text)

    def visit_title(self, node):
        title_functions = [self.emit_title, self.emit_chapter, self.emit_section, self.emit_subsection]
        try:
            f = title_functions[self.section_level]
        except exceptions.IndexError:
            f = self.emit_subsection
            #self.body.append('@c section_level %d' % self.section_level)
        f(node.astext())
        raise nodes.SkipNode

    def visit_paragraph(self, node):
        self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_bullet_list(self, node):
        self.body.append('@itemize @bullet')

    def depart_bullet_list(self, node):
        self.body.append('@end @itemize')

    def visit_list_item(self, node):
        self.body.append('@item')

    def depart_list_item(self, node):
        self.body.append('')

    def visit_literal(self, node):
        raise nodes.SkipNode

    def visit_literal_block(self, node):
        self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_block_quote(self, node):
        self.body.append('@quotation')
        #self.body.append(node.astext())

    def depart_block_quote(self, node):
        self.body.append('@end quotation')
