#!/usr/bin/env python

import postmarkup

import sys

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class PyTag(postmarkup.TagBase):

    DEFAULT_NAME = "py"

    def __init__(self, name, **kwargs):
        postmarkup.TagBase.__init__(self, name, enclosed=True, inline=True, strip_first_newline=True)

    def render_open(self, parser, node_index):

        tag_data = parser.tag_data
        globals = tag_data.setdefault("EvalTag.globals", {})
        locals = tag_data.setdefault("EvalTag.locals", {})

        contents = self.get_contents(parser).strip()
        self.skip_contents(parser)

        stdout = sys.stdout
        contents = "\n".join(contents.split('\r\n')) + "\n"

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

        if not self.params.lower() == "safe":
            result = postmarkup._escape(result)

        return result.rstrip()


class EvalTag(postmarkup.TagBase):

    DEFAULT_NAME = "eval"

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
                result = "(Error in eval tag)"

        if not self.params.lower() == "safe":
            result = postmarkup._escape(result)

        return result.rstrip()

class InlineCodeTag(postmarkup.TagBase):

    DEFAULT_NAME = "c"

    def __init__(self, name, **kwargs):
        postmarkup.TagBase.__init__(self, name, inline=True)

    def render_open(self, parser, node_index):
        return u"<code>"

    def render_close(self, parser, node_index):
        return u"</code>"

class PostLinkTag(postmarkup.TagBase):

    DEFAULT_NAME = "url"

    def __init__(self, name, **kwargs):
        super(PostLinkTag, self).__init__(name, annotate_links=False, **kwargs)

    def render_open(self, parser, node_index):

        external_link = ':' in self.params

        if external_link:
            domain = postmarkup.LinkTag._re_domain.search(self.params.lower()).group(1)
            return u'<a href="%s" class="external-link" title="%s">' % (self.params, domain)
        else:
            return u'<a href="%s">' % (self.params)

    def render_close(self, parser, node_index):

        return u"</a>"


class MoreTag(postmarkup.TagBase):

    DEFAULT_NAME = "more"

    def __init__(self, name, **kwargs):
        super(MoreTag, self).__init__(name, auto_close=True, **kwargs)

    def render_open(self, parser, node_index):
        return u"<!--more-->"

#
#class HTMLTag(postmarkup.TagBase):
#
#    DEFAULT_NAME = "html"
#
#    def __init__(self, name, **kwargs):
#        postmarkup.TagBase.__init__(self, name, enclosed=True, strip_first_newline=True)
#
#
#    def render_open(self, parser, node_index):
#        contents = self.get_contents(parser).strip()
#        self.skip_contents(parser)
#        return contents
#
#class SummaryTag(postmarkup.TagBase):
#
#    DEFAULT_NAME = "summary"
#
#    def __init__(self, name, **kwargs):
#        postmarkup.TagBase.__init__(self, name, inline=True)
#
#    def render_close(self, parser, node_index):
#        contents = self.get_contents(parser).strip()
#        tag_data = parser.tag_data
#        summary = tag_data["output"].setdefault("summary", "")
#        tag_data["output"]["summary"] = contents
#        return u""
#
#class AnchorTag(postmarkup.TagBase):
#
#    DEFAULT_NAME = "anchor"
#
#    def __init__(self, name, **kwargs):
#        postmarkup.TagBase.__init__(self, name, autoclose=True, inline=True)
#
#    def render_open(self, parser, node_index):
#        anchor_name = self.params.lower().replace(' ', '_')
#        return u"""<a name="%s" />""" % anchor_name
#
#class PullquoteTag(postmarkup.TagBase):
#
#    DEFAULT_NAME = "pullquote"
#
#    def __init__(self, name, **kwargs):
#        postmarkup.TagBase.__init__(self, name, inline=False)
#
#    def render_open(self, parser, node_index):
#        contents = self.get_contents(parser).strip()
#        self.skip_contents(parser)
#        txt = postmarkup._escape(contents)
#        html = u"""<div class="pullquote">"%s"</div>""" % txt
#        return html
#
#class PulloutTag(postmarkup.TagBase):
#
#    DEFAULT_NAME = "pullout"
#
#    def __init__(self, name, **kwargs):
#        postmarkup.TagBase.__init__(self, name, inline=False)
#
#    def render_open(self, parser, node_index):
#        left = self.params.lower() != 'right'
#        if left:
#            return """<div class="pullout-left">"""
#        else:
#            return """<div class="pullout-right">"""
#
#    def render_close(self, parser, node_index):
#        return """</div>"""
