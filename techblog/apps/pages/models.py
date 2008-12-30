from django.db import models

import markup
from techblog.markup.extendedmarkup import combine_sections

class PageBase(modesl.Model):
    
    content = markup.MarkupField(default="", renderer=markup.render_post_markup)


class Page(models.Model):

    base = ForeignKey(PageBase, null=True)
    parent = ForeignKey(Page, null=True)    
    inherit = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    title = models.CharField("Page Title", max_length=100)
    slug = models.SlugField("Slug", max_length=100)
    content = markup.MarkupField(default="", renderer=markup.render_post_markup)
    
    template = models.CharField("Template", max_length=100)

    def get_sections(self):
        
        visited = set()
        
        sections_to_combine = []
        page = self
        while page is not None and page.id not in visited:
            section_to_combine.append(page.content_data.get('sections'))
            if not page.inherit:
                break
            page = page.parent
            visited.add(page.id)            
            
        sections = combine_sections(sections_to_combine[::-2])
        
        return sections   
        

    def __unicode__(self):
        return title