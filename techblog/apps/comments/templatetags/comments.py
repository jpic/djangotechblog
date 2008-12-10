from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.contenttypes.models import ContentType

from techblog.apps.comments import forms
from techblog.apps.comments import models

import urllib, hashlib

import re

register = template.Library()

@register.simple_tag
def comment_form(object, css_class=None):

    initial_data = {}

    initial_data['object_id'] = str(object.id)

    ct = ContentType.objects.get_for_model(object)
    ct_id = ".".join( (ct.app_label, ct.model) )
    initial_data['content_type'] = ct_id
    initial_data['success_url'] = object.get_absolute_url()

    comment_form = forms.CommentForm(initial=initial_data)

    if css_class is None:
        return '<div>%s</div>' % comment_form.as_p()
    else:
        return '<div class="%s">%s</div>' % (css_class, comment_form.as_p())





_re_comments_tag = re.compile(r'for (?P<object>\w+) as (?P<name>\w+)')


class GetCommentFormNode(template.Node):
    def __init__(self, object_name, value_name):
        self.object_name = object_name
        self.value_name = value_name

    def render(self, context):

        object = context.get(self.object_name, None)

        if object is None:
            return ''
        ct = ContentType.objects.get_for_model(object)

        initial_data = {}

        initial_data['object_id'] = str(object.id)
        ct_id = ".".join( (ct.app_label, ct.model) )
        initial_data['content_type'] = ct_id
        initial_data['success_url'] = object.get_absolute_url()
        comment_form = forms.CommentForm(initial=initial_data)

        context[self.value_name] = comment_form

        return ''

@register.tag
def get_comment_form(parser, token):

    directive = token.contents.strip().split(' ', 1)[1]

    match = _re_comments_tag.match(directive)

    if match is None:
        raise template.TemplateSyntaxError("Syntax error")

    object_name = match.group(1)
    value_name = match.group(2)

    return GetCommentFormNode(object_name, value_name)



class GetCommentsNode(template.Node):
    def __init__(self, object_name, value_name):
        self.object_name = object_name
        self.value_name = value_name

    def render(self, context):

        object = context.get(self.object_name, None)
        if object is None:
            return ''
        ct = ContentType.objects.get_for_model(object)
        comments = models.Comment.objects.filter(object_id=object.id, content_type=ct, visible=True, moderated=True)
        context[self.value_name] = comments
        return ''

@register.tag
def get_comments(parser, token):

    directive = token.contents.strip().split(' ', 1)[1]

    match = _re_comments_tag.match(directive)

    if match is None:
        raise template.TemplateSyntaxError("Syntax error")

    object_name = match.group(1)
    value_name = match.group(2)

    return GetCommentsNode(object_name, value_name)


@register.simple_tag
def gravatar(email, size=None, default=None):

    size = size or 40
    gravatar_url = "http://www.gravatar.com/avatar.php?"

    params = {'gravatar_id':hashlib.md5(email).hexdigest(), 'size':str(size)}
    if default is not None:
        params['default'] = default

    gravatar_url += urllib.urlencode(params)
    return '<img width="%d" height="%d" class="gravatar" src="%s">' % (size, size, gravatar_url)
