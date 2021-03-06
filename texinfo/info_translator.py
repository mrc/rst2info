from docutils import nodes
import exceptions
import string

class InfoTranslator(nodes.NodeVisitor):

    document_start = """\\input texinfo  @c -*-texinfo-*-
"""
    
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        self.header = []
        self.body = []
        self.section_level = 0
        self.system_message_level = 0
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

    def visit_subtitle(self, node):
        self.body.append('@majorheading %s' % node.astext())
        raise nodes.SkipNode

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self.system_message_level == 0:
            self.body.append('')

    def visit_bullet_list(self, node):
        self.body.append('@itemize @bullet')

    def depart_bullet_list(self, node):
        self.body.append('@end @itemize')
        self.body.append('')

    def visit_enumerated_list(self, node):
        start = 1
        if node.has_key('start'):
            start = node['start']
        if node.has_key('enumtype'):
            if node['enumtype'] == 'upperalpha':
                start =string.ascii_uppercase[start-1]
            if node['enumtype'] == 'loweralpha':
                start =string.ascii_lowercase[start-1]
        self.body.append('@enumerate %s' % start)

    def depart_enumerated_list(self, node):
        self.body.append('@end enumerate')
        self.body.append('')

    def visit_list_item(self, node):
        self.body.append('@item')

    def depart_list_item(self, node):
        pass

    def visit_literal(self, node):
        raise nodes.SkipNode

    def visit_literal_block(self, node):
        self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_block_quote(self, node):
        self.body.append('@quotation')

    def depart_block_quote(self, node):
        self.body.append('@end quotation')
        self.body.append('')

    def visit_system_message(self, node):
        # from rst2man
        if node['level'] < self.settings.report_level:
            raise nodes.SkipNode
        attr = {}
        backref_text = ''
        if node.hasattr('id'):
            attr['name'] = node['id']
        if node.hasattr('line'):
            line = ', line %s' % node['line']
        else:
            line = ''
        self.body.append('@c System Message: %s/%s (%s:%s)'
                         % (node['type'], node['level'], node['source'], line))
        self.system_message_level += 1

    def depart_system_message(self, node):
        self.system_message_level -= 1
        self.body.append('@c --end system message--')

    def visit_definition_list(self, node):
        pass

    def depart_definition_list(self, node):
        pass

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_term(self, node):
        pass

    def depart_term(self, node):
        pass

    def visit_definition(self, node):
        self.body.append('@quotation')

    def depart_definition(self, node):
        self.body.append('@end quotation')
        self.body.append('')

    def visit_Text(self, node):
        if self.system_message_level > 0:
            self.body.append('@c %s' % node.astext())
        else:
            self.body.append(node.astext())

    def depart_Text(self, node):
        pass
