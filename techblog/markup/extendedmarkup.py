#!/usr/bin/env python

#!/usr/bin/env python

import postmarkup

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.template.loader import get_template, select_template
from django.template.context import Context

import re

postmarkup_renderer = postmarkup.create()

class ExtendedMarkupError(Exception):
    pass

def render_postmarkup(text):
    tag_tada = {}
    postmarkup_renderer(text, paragraphs=False)

class Chunk(object):

    def __init__(self, text, chunk_type='text'):
        self.text = text
        self.chunk_type = chunk_type
        self.vars = {}

    def __str__(self):
        return "%s: %s, %s" % (self.chunk_type, repr(self.text), repr(self.vars))

    def __iter__(self):
        return iter(self.text)

    def __cmp__(self, other):
        def priority(s):
            try:
                return int(s)
            except:
                return s
        return -cmp( self.get_priority(), other.get_priority() )

    def get_priority(self):
        try:
            return int(self.vars.get('priority', '100'))
        except:
            return 100

    __repr__ = __str__


class Section(list):

    def __init__(self, name, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self.vars = {}
        self.name = name

    def __str__(self):
        return "%s, %s" % ( repr(list(self)), self.vars )

    __repr__ = __str__


class EMarkupParser(object):


    re_extended_directive = re.compile(r"^\{.+?\}$")

    def __init__(self, renderer=None):
        if renderer is None:
            self.renderer = postmarkup.create()

    def parse(self, text, default_section = "main", default_chunk_type = "paragraph"):


        self._current_section = ""
        self._default_section = default_section
        self._current_chunk_type = ""
        self._default_chunk_type = default_chunk_type

        self.sections = {}
        sections = self.sections

        self._chunks = []
        chunks = self._chunks

        self.current_lines = []
        current_lines = self.current_lines

        new_chunk = True

        self.vars = {}
        vars = self.vars

        self._section_vars = {}
        self._chunk_vars = {}

        comment_mode = 0

        def make_chunk():
            if current_lines:
                chunk = current_lines[:]
                chunk = Chunk(chunk, self._current_chunk_type.strip() or self._default_chunk_type)
                chunk.vars.update(self._chunk_vars)
                self._chunk_vars.clear()
                chunks.append(chunk)
                del current_lines[:]

        def process_vars(vars, line):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                vars[key] = value
                return True
            return False

        lines = [line.rstrip() for line in text.replace('\r', '').split('\n')]
        for line_no, line in enumerate(lines):

            if not line:
                current_lines.append("");
                new_chunk = True
                continue

            if new_chunk:

                if line == ';/*':
                    comment_mode += 1
                    continue

                elif line == ';*/':
                    if comment_mode:
                        comment_mode -= 1
                    continue

                if comment_mode:
                    continue

                if line.startswith(';//'):
                    continue

                if self.re_extended_directive.match(line):

                    line = line[1:-1]
                    # Chunk type
                    if line.startswith('..'):
                        line = line[2:]
                        if not process_vars(self._chunk_vars, line):
                            make_chunk()
                            self._current_chunk_type = line or default_chunk_type
                        continue

                    # Section
                    elif line.startswith('.'):
                        line = line[1:]
                        if not process_vars(self._section_vars, line):
                            make_chunk()
                            section_name = line or default_section
                            self.set_section(section_name)
                        continue

                    else:
                        process_vars(vars, line)
                        continue

                else:
                    current_lines.append(line)
                    continue

                new_chunk = False

            current_lines.append(line)
            new_chunk = False

        make_chunk()
        self.set_section(None)

        return self.sections

    __call__ = parse

    def set_section(self, section_name):

        current_section = self._current_section or self._default_section
        section = self.sections.setdefault(current_section, Section(current_section))

        section.vars.update(self._section_vars)
        section += self._chunks
        del self._chunks[:]

        self._current_section = section_name or self._default_section
        self._current_chunk_type = self._default_chunk_type

        self._section_vars = {}


def parse(markup, sections=None):

    parser = EMarkupParser()
    parser.parse(markup)
    sections = parser.sections
    vars = parser.vars

    rendered_sections = sections or {}

    error_template = select_template(['markupchunks/error.html'])

    for section, chunks in sections.iteritems():

        content_chunks = []

        for chunk in chunks:

            chunk_filename = "markupchunks/%s.html" % chunk.chunk_type.encode()
            chunk_template = select_template([chunk_filename, "markupchunks/paragraph.html"])

            chunk_data = dict(chunk=chunk, content="\n".join(chunk))
            try:
                chunk_html = chunk_template.render(Context(chunk_data))
            except Exception, e:
                error = str(e)
                chunk_html = error_template.render(Context(dict(error=error)))

            content_chunks.append((chunk.get_priority(), chunk_html))

        rendered_sections[section] = content_chunks

    return rendered_sections

def chunks_to_html(chunks):
    return "\n".join( chunk[1] for chunk in sorted(chunks, key=lambda chunk:chunk[0]) )

def combine_sections(*sections_list):

    combined = {}
    for sections in filter(None, sections_list):

        for name_section in sections.iteritems():
            if name_section is None:
                continue

            section_name, section = name_section

            if section_name not in combined:
                new_section = Section(section_name)
                combined[section_name] = new_section

            combined[section_name] += section

    return combined

if __name__ == "__main__":
    test = """;hello=world

;.title
This is the title

;.body
;.template=test.html

This is in the body

This is also in the body

;..pullquote
;..location=left

This is in a pullquote

This is also in a pullquote


;..code
;..lang=python

    elif line.startswith('*/'):
        if comment_mode:
            comment_mode -= 1
        continue

    if comment_mode:
        continue

.

import


"""


    test=""".main
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Cras non tortor. Sed nunc. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Duis vitae eros. Phasellus dui nisl, porta sed, tristique non, feugiat eu, metus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Duis tincidunt est sit amet quam. Praesent lacus mauris, lacinia vitae, suscipit ac, dignissim ut, massa. Sed rutrum, magna consectetuer sollicitudin auctor, urna tortor suscipit dolor, ac suscipit dui eros gravida erat. Morbi molestie, ligula vitae sagittis adipiscing, felis risus laoreet metus, nec accumsan sem libero ut elit. Pellentesque augue nibh, sollicitudin eu, porttitor sit amet, ultricies quis, odio. Nam id est. Nunc libero urna, hendrerit ut, suscipit et, mollis id, mi. Praesent lobortis leo at neque. Vivamus mattis aliquet ligula. Duis dui sem, posuere eu, porta ac, hendrerit et, ante. Nulla porttitor magna vel ante pharetra viverra.

.column2
..module
..title=This is a Module
This should be displayed inside a module box in column2"""


    #emarkup = EMarkupParser()
    #sections = emarkup(test)

    import os
    import sys
    sys.path.append("/home/will/projects/djangotechblog")
    os.environ["DJANGO_SETTINGS_MODULE"] = "techblog.settings"

    sections = parse(test)

    import pprint
    #pprint.pprint(sections)

    for section, html in sections.iteritems():
        print "<h1>%s</h1>" % section
        print html
    pprint.pprint(sections)
    #pprint.pprint(emarkup.vars)
