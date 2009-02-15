from django import template
from django.template.defaultfilters import stringfilter
import re

from techblog.apps.resources import models

register = template.Library()


def parse_dimensions(d):

    def to_int(s):
        try:
            return int(s)
        except ValueError:
            return None

    values = map(to_int, d.split()[:2])

    if not values:
        return None, None

    if len(values) == 1:
        return values[0], None

    return values

@register.simple_tag
def siteimage_width(name, dimensions):

    width, height = parse_dimensions(dimensions)
    return str(width or '')

@register.simple_tag
def siteimage_url(name, dimensions):

    width, height = parse_dimensions(dimensions)

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
def siteimage(name, dimensions):

    width, height = parse_dimensions(dimensions)

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

    html = '<img src="%s" width="%i" height="%i" alt="%s" title="%s"></img>' % (url, width, height, img_upload.description, img_upload.description)

    return html
