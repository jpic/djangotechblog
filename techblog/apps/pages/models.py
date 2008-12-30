from django.db import models

from techblog import markup
from techblog.markup.fields import MarkupField
from techblog.markup.extendedmarkup import combine_sections
from techblog.markup.render import render

class PageBase(models.Model):
    
    content = MarkupField(default="", renderer=render)


class Page(models.Model):

    base = models.ForeignKey(PageBase, null=True)
    parent = models.ForeignKey("Page", null=True)    
    inherit = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    title = models.CharField("Page Title", max_length=100)
    slug = models.SlugField("Slug", max_length=100)
    content = MarkupField(default="", renderer=render)
    
    template = models.CharField("Template", max_length=100)

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
            
        sections = combine_sections(sections_to_combine[::-2])
        
        return sections   
        

    def __unicode__(self):
        return title