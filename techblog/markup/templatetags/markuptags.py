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
def markupsection(sections, key):

    if not sections:
        return u""
    chunks = sections.get(key)

    if chunks is None:
        return u""

    print type(chunks[0])
    print chunks[0]

    return mark_safe( u"\n".join(chunk.text for chunk in sorted(chunks, key=lambda chunk:chunk.get_priority()) if chunk )  )

@register.simple_tag
def code(content, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
    except ClassNotFound:
        content = postmarkup._escape(content)
        return '<div class="code"><pre>%s</pre></div>' % content

    formatter = HtmlFormatter(linenos=False, cssclass="code")
    highlighted = highlight(content, lexer, formatter).strip()

    return mark_safe( highlighted )

@register.simple_tag
def code_linenumbers(content, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
    except ClassNotFound:
        content = postmarkup._escape(content)
        return '<div class="code"><pre>%s</pre></div>' % content

    formatter = HtmlFormatter(linenos=True, cssclass="code")
    return mark_safe( highlight(content, lexer, formatter).strip() )

@register.filter
@stringfilter
def link(link):
    if '|' not in link:
        return link
    text, url = link.split('|', 1)
    text = text.strip()
    url = url.strip()

    return mark_safe('<a href="%s">%s</a>' % (url, text))