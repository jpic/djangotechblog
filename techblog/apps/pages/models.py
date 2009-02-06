from django.db import models

from techblog import markup
from techblog.markup.fields import MarkupField
from techblog.markup.extendedmarkup import combine_sections
from techblog.markup.render import render

class PageBase(models.Model):

    name = models.CharField("Name", default="", blank=True, max_length=255)
    template = models.CharField("Page template", default="", blank=True, max_length=255)

    def __unicode__(self):
        return self.name

class PublishedPageManager(models.Manager):

    def get_query_set(self):
        return super(PublishedPageManager, self).get_query_set().filter(published=True)


class Page(models.Model):

    base = models.ForeignKey(PageBase, blank=True, null=True)
    parent = models.ForeignKey("Page", blank=True, null=True)
    path = models.CharField("Page path", max_length=255, blank=True)

    title = models.CharField("Page Title", max_length=100)
    slug = models.SlugField("Slug", max_length=100, db_index=True)

    inherit = models.BooleanField("Inherit parent's content?", default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField("Display on site?", default=False)
    promoted = models.BooleanField("Display in children list?", default=True)


    content = MarkupField(default="", blank=True, renderer=render)

    published_pages = PublishedPageManager()

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

        return templates

    @models.permalink
    def get_absolute_url(self):

        return ("apps.pages.views.page", (),
                dict(path=self.path))

    def save(self, *args, **kwargs):
        self.create_path()
        return super(Page, self).save(*args, **kwargs)

    def create_path(self):

        pages_checked = set()
        page = self
        page_components = []

        while page is not None and page.id not in pages_checked:
            page_components.append(page.slug)
            pages_checked.add(page.id)
            page = page.parent

        path = "/".join(page_components[::-1])
        self.path = path


    @classmethod
    def page_from_path(cls, path):

        components = path.split('/')

        page = None
        for component in components:
            try:
                page = Page.objects.get(slug=component, parent=page)
            except Page.DoesNotExist:
                return None
        return page

    def get_children(self):

        children = Page.published_pages.all()
        return children

    def get_promoted_children(self):

        children = self.get_children().filter(promoted=True)
        return children
