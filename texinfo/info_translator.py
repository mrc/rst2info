from docutils import nodes

class InfoTranslator(nodes.NodeVisitor):

    document_start = '\\input texinfo  @c -*-texinfo-*-'
    
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
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

    def depart_section(self, node):
        self.section_level -= 1

    def visit_title(self, node):
        self.body.append('@node %s' % node.astext())
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

    def depart_literal_block(self, node):
        pass