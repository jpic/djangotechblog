from django import template
from django.template.defaultfilters import stringfilter

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