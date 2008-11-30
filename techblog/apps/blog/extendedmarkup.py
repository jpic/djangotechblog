#!/usr/bin/env python

import postmarkup

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

postmarkup_renderer = postmarkup.create()

def render_postmarkup(text):
    tag_tada = {}
    postmarkup_renderer(text, paragraphs=False)

class EMarkup(object):

    def __init__(self, renderer=None):
        if renderer is None:
            self.renderer = postmarkup.create()

    def render(text):

        lines = StringIO(text)

        sections = {}
        self.current_section = "main"
        chunks = []
        current_lines = []

        line_no = 0
        blank_count = 2


        while True:

            line = lines.readline()
            blank_line = bool(line.strip())
            if blank_line:
                blank_count += 1
            else:
                blank_count = 0

            if blank_count > 1:

                if line.startswith('.'):
                    
                    directive_name, data = line.split(' ', 1)
                    directive_name = directive.lower().strip()
                    data = data.strip()

                    directive_func = getattr(self, "directive_"+directive_name, None)
                    if directive_func is not None:
                        directive_func()

                else:
                    chunk_text = "".join(current_lines)
                    del current_lines[:]

                    sections.setdefault(current_section, [])
                    sections[current_section].append(chunk_text)

                    chunks.append(chunk_text)

            else:

                chunks.append(line)


    def set_section(self, section_name):

        self.current_section = section_name

    def directive_in(self, data):

        section_name = data.split(' ', 1).strip()
        if section_name:
            self.set_section(section_name)
