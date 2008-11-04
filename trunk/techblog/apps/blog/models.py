from django.db import models
from django.contrib.auth.models import User
from fields import PickledObjectField
from django.utils.safestring import mark_safe
import datetime

import markup


# Create your models here.



class Blog(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField("Title of the Blog", max_length=100)
    slug = models.SlugField()

    markup_type = models.CharField(choices=markup.MARKUP_TYPES, default="postmarkup", max_length=20)
    markup_raw = models.TextField(default="")
    html = models.TextField(default="", blank=True)
    text = models.TextField(default="", blank=True)
    data = PickledObjectField(default={}, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        markup.render_post_markup(self)
        super(Post, self).save(force_insert, force_update)


#markup.add_markup_to_model(Blog, "description", "Blog description markup", markup.render_blogpost)


class Post(models.Model):

    title = models.CharField("Post Title", max_length=100)
    slug = models.SlugField("Post Slug")
    published = models.BooleanField("Published?", default=False)


    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    display_time = models.DateTimeField("Post Time", default=datetime.datetime.now)


    markup_type = models.CharField("Markup Type", choices=markup.MARKUP_TYPES, default="postmarkup", max_length=20)
    markup_raw = models.TextField(default="")
    html = models.TextField(default="", blank=True)
    text = models.TextField(default="", blank=True)
    data = PickledObjectField(default={}, blank=True)

    #created_time = models.DateTimeField(auto_now_add=True)

    def get_admin_abbrev(self):
        if len(self.text) < 100:
            return self.text
        return self.text[:100]+" [...]"
    get_admin_abbrev.short_description = "Content (abbreviated)"

    def get_admin_html(self):
        return self.html
    get_admin_html.allow_tags = True

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        markup.render_post_markup(self)
        super(Post, self).save(force_insert, force_update)

#markup.add_markup_to_model(Post, "content", "Post content", markup.render_blogpost)