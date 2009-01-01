from django.db import models

from techblog import markup
from techblog.markup.fields import MarkupField
from techblog.markup.extendedmarkup import combine_sections
from techblog.markup.render import render

class PageBase(models.Model):

    name = models.CharField("Name", default="", blank=True, max_length=255)
    content = MarkupField(default="", renderer=render)
    template = models.CharField("Page template", default="", blank=True, max_length=255)

    def __unicode__(self):
        return self.name

class Page(models.Model):

    base = models.ForeignKey(PageBase, blank=True, null=True)
    parent = models.ForeignKey("Page", blank=True, null=True)
    path = models.CharField("Page path", max_length=255)
    inherit = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    title = models.CharField("Page Title", max_length=100)
    slug = models.SlugField("Slug", max_length=100)
    content = MarkupField(default="", blank=True, renderer=render)

    #allow_comments = mdoels.BooleanField(default=False)

    def __unicode__(self):
        return self.path

    def get_sections(self):

        visited = set()

        sections_to_combine = []
        page = self
        while page is not None and page.id not in visited:
            visited.add(page.id)
            sections_to_combine.append(page.content_data.get('sections'))
            if not page.inherit:
                break
            page = page.parent

        sections_to_combine = sections_to_combine[::-1]

        if self.base is not None:
            sections_to_combine.append(self.base.content_data.get('sections'))

        sections = combine_sections( *sections_to_combine )

        return sections

    def get_template_names(self):

        templates = ["page/page.html"]
        if self.base and self.base.template:
            templates.insert(0, self.base.template)

        print templates

        return templates

    @models.permalink
    def get_absolute_url(self):

        return ("apps.pages.views.page", (),
                dict(path=self.path))