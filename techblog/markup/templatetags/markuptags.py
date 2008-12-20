from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re

from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import HtmlFormatter

        #try:
        #    lexer = get_lexer_by_name(self.params, stripall=True)
        #except ClassNotFound:
        #    contents = _escape(contents)
        #    return '<div class="code"><pre>%s</pre></div>' % contents
        #
        #formatter = HtmlFormatter(linenos=self.line_numbers, cssclass="code")
        #return highlight(contents, lexer, formatter).strip().replace("\n", "<br/>")

register = template.Library()

from postmarkup import render_bbcode

@register.filter
@stringfilter
def postmarkup(value):
    if not value:
        return u""
    html = mark_safe(render_bbcode(value))
    return html

@register.simple_tag
def markupsection(chunk_dict, key):

    if not chunk_dict:
        return u""
    chunks = chunk_dict.get(key, [])

    return mark_safe( u"\n".join(chunk[1] for chunk in sorted(chunks, key=lambda chunk:chunk[0]) if chunk )  )

@register.simple_tag
def code(content, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
    except ClassNotFound:
        content = postmarkup._escape(content)
        return '<div class="code"><pre>%s</pre></div>' % content

    formatter = HtmlFormatter(linenos=False, cssclass="code")
    return mark_safe( highlight(content, lexer, formatter).strip() )

@register.simple_tag
def code_linenumbers(content, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
    except ClassNotFound:
        content = postmarkup._escape(content)
        return '<div class="code"><pre>%s</pre></div>' % content

    formatter = HtmlFormatter(linenos=True, cssclass="code")
    return mark_safe( highlight(content, lexer, formatter).strip() )