from django.db import models

from techblog.apps.markup import MarkupField


class Page(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    title = models.CharField("Page Title", max_length=100)
    content = MarkupField("Page content")
