#!/usr/bin/env python

import postmarkup

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

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

    __repr__ = __str__

class Section(list):

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self.vars = {}


class EMarkupParser(object):

    def __init__(self, renderer=None):
        if renderer is None:
            self.renderer = postmarkup.create()

    def parse(self, text, default_section = "main", default_chunk_type = "text"):


        lines = StringIO(text)

        self._current_section = default_section
        self._default_section = default_section
        self._default_chunk_type = default_chunk_type
        self._current_chunk_type = default_chunk_type

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
            if comment_mode:
                return
            if current_lines:
                chunk = "\n".join(current_lines)
                chunk = Chunk(chunk, self._current_chunk_type)
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
            else:
                vars[line.strip()] = '1'

        for line_no, line in enumerate(lines):

            line = line.rstrip()
            if not line:
                new_chunk = True
                continue

            if new_chunk:


                make_chunk()

                # Chunk vars

                if line.startswith('/*'):
                    comment_mode += 1
                    continue

                elif line.startswith('*/'):
                    if comment_mode:
                        comment_mode -= 1
                    continue

                if comment_mode:
                    continue

                if line.startswith('//'):
                    continue

                elif line.startswith('..?'):
                    line = line[3:]
                    process_vars(self._chunk_vars, line)
                    continue

                # Section vars
                elif line.startswith('.?'):
                    line = line[2:]
                    process_vars(self._section_vars, line)
                    continue

                # Chunk type
                elif line.startswith('..'):
                    self._current_chunk_type = line[2:] or default_chunk_type
                    continue

                # Section
                elif line.startswith('.'):
                    section_name = line[1:] or default_section
                    self.set_section(section_name)
                    continue

                ## Directive
                #elif line.startswith('.!'):
                #    directive_name, data = line[2:].split(' ', 1)
                #    directive_name = directive_name.lower().strip()
                #    data = data.strip()
                #
                #    directive_func = getattr(self, "directive_"+directive_name, None)
                #    if directive_func is not None:
                #        directive_func(directive_name, data)
                #    continue

                elif line.startswith('?'):
                    line = line[1:]
                    process_vars(vars, line)

                else:
                    current_lines.append(line)

                new_chunk = False
                continue


            current_lines.append(line)
            new_chunk = False

        make_chunk()
        self.set_section(None)

        return self.sections

    __call__ = parse

    def set_section(self, section_name):

        section = self.sections.setdefault(self._current_section, Section())
        self.sections[self._current_section].vars.update(self._section_vars)
        section += self._chunks
        del self._chunks [:]

        self._current_section = section_name or self._default_section
        self._current_chunk_type = self._default_chunk_type

        self._section_vars = {}



if __name__ == "__main__":
    test = """.title
This is the title

/*
This is a comment
*/
// This is also a comment

.body

This is a pragraph, with [b]bbcode[/b]..

.main
.?a section var
..html
..?avar
This is part of the same paragraph


This is a another [i]paragraph[/i]

.plain

Oh Hai!


..code python

import this

;This is a comment
..html
<a href="#">Hello, World!</a>

..
Not python code

?will=cool

.sidebar

This is sidebar content

"""

    emarkup = EMarkupParser()
    sections = emarkup(test)

    import pprint
    pprint.pprint(emarkup.sections)
    pprint.pprint(emarkup.vars)
