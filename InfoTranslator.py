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
        return ''.join(self.header + self.body)
    
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

'''
    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        pass

    def visit_list_item(self, node):
        pass

    def depart_list_item(self, node):
        pass
'''
