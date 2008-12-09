from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from techblog.apps.blog.fields import MarkupField

from techblog import broadcast

# Create your models here.


def _comment_renderer(markup, markup_type):

    html, summary_html, text, data = broadcast.call.render_comment(markup, markup_type)
    return html, summary_html, text, data

class Comment(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    visible = models.BooleanField(default=False)
    moderated = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)

    name = models.CharField("Author's name", max_length=100)
    email = models.EmailField("Author's email")
    url = models.URLField(verify_exists=False, default="")
    content = MarkupField(default="", renderer=_comment_renderer)
