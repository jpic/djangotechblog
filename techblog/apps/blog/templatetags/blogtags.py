from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


short_months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
long_months = "January February March April May June July August September October November December".split()

@register.filter
@stringfilter
def shortmonth(value):
    try:
        month_index = int(value)
    except ValueError:
        return "INVALID MONTH"

    return short_months[month_index-1]


@register.filter
@stringfilter
def longmonth(value):
    try:
        month_index = int(value)
    except ValueError:
        return "INVALID MONTH"

    return long_months[month_index-1]

_re_first_paragraph = re.compile(r"<p>.*?</p>")

@register.filter
@stringfilter
def first_paragraph(value):
    match = _re_first_paragraph.match(value)
    if not match:
        return value
    return match.group(0)


@register.filter
@stringfilter
def smart_title(value):
    def title(word):
        for c in word:
            if c.isupper():
                return word
        return word.title()
    return u" ".join(title(value) for value in value.split())
