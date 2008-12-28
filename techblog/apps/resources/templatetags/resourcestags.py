from django import template
from django.template.defaultfilters import stringfilter
import re

from techblog.apps.resources import models

register = template.Library()


@register.simple_tag
def siteimage_url(name, width=None, height=None):

    try:
        img_upload = models.ImageUpload.objects.get(name__iexact=name)
    except models.ImageUpload.DoesNotExist:
        raise template.TemplateSyntaxError("Unknown image (%s)" % str(name))

    if width is not None:
        try:
            width = int(width)
        except ValueError:
            raise template.TemplateSyntaxError("Width must be a number")

    if height is not None:
        try:
            height = int(height)
        except ValueError:
            raise template.TemplateSyntaxError("Height must be a number")

    url = img_upload.image.url

    return url



@register.simple_tag
def siteimage(name, width=None, height=None):

    try:
        img_upload = models.ImageUpload.objects.get(name__iexact=name)
    except models.ImageUpload.DoesNotExist:
        raise template.TemplateSyntaxError("Unknown image (%s)" % str(name))

    if width is not None:
        try:
            width = int(width)
        except ValueError:
            raise template.TemplateSyntaxError("Width must be a number")

    if height is not None:
        try:
            height = int(height)
        except ValueError:
            raise template.TemplateSyntaxError("Height must be a number")

    url = img_upload.thumb(width, height)

    html = '<img src="%s" alt="%s" title="%s"></img>' % (url, img_upload.description, img_upload.description)

    return html
