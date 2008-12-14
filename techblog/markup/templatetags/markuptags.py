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
    return mark_safe(render_bbcode(value))