#!/usr/bin/env python

import postmarkup

import sys

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class PyTag(postmarkup.TagBase):

    def __init__(self, name, **kwargs):
        postmarkup.TagBase.__init__(self, name, enclosed=True, strip_first_newline=True)

    def render_open(self, parser, node_index):

        tag_data = parser.tag_data
        globals = tag_data.setdefault("EvalTag.globals", {})
        locals = tag_data.setdefault("EvalTag.locals", {})

        contents = self.get_contents(parser).strip()
        self.skip_contents(parser)

        stdout = sys.stdout

        contents = "\n".join(contents.split('\r\n')) + "\n"

        print repr(contents)

        sys.stdout = StringIO()


        try:
            try:
                try:
                    exec contents in globals, locals
                except Exception, e:
                    result = str(e)
            except:
                result = ""
        finally:
            result = sys.stdout.getvalue()
            sys.stdout = stdout

        return result.rstrip()


class EvalTag(postmarkup.TagBase):

    def __init__(self, name, **kwargs):
        postmarkup.TagBase.__init__(self, name, inline=True, enclosed=True, strip_first_newline=True)

    def render_open(self, parser, node_index):

        tag_data = parser.tag_data
        globals = tag_data.setdefault("EvalTag.globals", {})
        locals = tag_data.setdefault("EvalTag.locals", {})

        contents = self.get_contents(parser).strip()
        self.skip_contents(parser)

        try:
            result = str(eval(contents, globals, locals))
        except Exception, e:
            try:
                result = str(e)
            except:
                retult = "(Error in eval tag)"

        return result.rstrip()

class HTMLTag(postmarkup.TagBase):

    def __init__(self, name, **kwargs):
        postmarkup.TagBase.__init__(self, name, enclosed=True, strip_first_newline=True)

    def open(self, parser, params, open_pos, node_index):
        parser.begin_no_breaks()
        return u""

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser).strip()
        self.skip_contents(parser)
        return contents

class SummaryTag(postmarkup.TagBase):

    def __init__(self, name, **kwargs):
        postmarkup.TagBase.__init__(self, name, strip_first_newline=True)

    def render_close(self, parser, node_index):
        contents = self.get_contents(parser).strip()
        tag_data = parser.tag_data
        summary = tag_data["output"].setdefault("summary", "")
        tag_data["output"]["summary"] = contents
        return u""
