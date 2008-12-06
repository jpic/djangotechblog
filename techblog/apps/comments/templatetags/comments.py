from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.contenttypes.models import ContentType

from techblog.apps.comments import forms

import re

register = template.Library()

@register.simple_tag
def comment_form(object, css_class=None):

    initial_data = {}

    initial_data['object_id'] = str(object.id)

    ct = ContentType.objects.get_for_model(object)
    ct_id = ".".join( (ct.app_label, ct.model) )
    initial_data['content_type'] = ct_id

    comment_form = forms.CommentForm(initial=initial_data)

    if css_class is None:
        return '<div>%s</div>' % comment_form.as_p()
    else:
        return '<div class="%s">%s</div>' % (css_class, comment_form.as_p())
