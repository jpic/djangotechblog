from django.db import models
from django.contrib.auth.models import User
from fields import PickledObjectField
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import datetime

import markup



class Tag(models.Model):

    blog = models.ForeignKey("Blog")
    name = models.CharField("Tag name", max_length=100)
    slug = models.SlugField()

    count = models.IntegerField(default="0", editable=False)

    def __unicode__(self):
        return self.name


class Channel(models.Model):

    title = models.CharField("Channel Title", max_length=100)
    tagline = models.CharField("Tag line", max_length=200)
    slug = models.SlugField()

    description = markup.MarkupField(default="", renderer=markup.render_post_markup)

    blogs = models.ManyToManyField("Blog")


class Blog(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField("Title of the Blog", max_length=100)
    tagline = models.CharField("Tag line", max_length=200)
    slug = models.SlugField()
    posts_per_page = models.IntegerField(default=10)

    description = markup.MarkupField(default="", renderer=markup.render_post_markup)

    def __unicode__(self):
        return self.title

    def posts(self):
        now = datetime.datetime.now()
        posts = self.post_set.filter(published=True,
                                     display_time__lte=now).order_by("display_time")
        return posts

    @models.permalink
    def get_absolute_url(self):

        blog_slug = self.slug

        return ("apps.blog.views.blog_front", (),
                dict(blog_slug=blog_slug))

class Post(models.Model):

    blog = models.ForeignKey(Blog)

    title = models.CharField("Post Title", max_length=100)
    slug = models.SlugField("Post Slug")
    published = models.BooleanField("Published?", default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    display_time = models.DateTimeField("Post Time", default=datetime.datetime.now)

    tags = models.ManyToManyField("Tag", blank=True)

    content = markup.MarkupField(default="", renderer=markup.render_post_markup)

    #created_time = models.DateTimeField(auto_now_add=True)

    def get_admin_abbrev(self):
        if len(self.content_text) < 100:
            return self.content_text
        return self.content_text[:100]+" [...]"
    get_admin_abbrev.short_description = "Content (abbreviated)"

    def get_admin_html(self):
        return self.html
    get_admin_html.allow_tags = True

    def __unicode__(self):
        return self.title

    def date_url(self):
        year = self.display_time.year
        month = self.display_time.month
        day = self.display_time.day
        return "%d/%d/%d/%s" % (year, month, day, self.slug)

    @models.permalink
    def get_absolute_url(self):

        blog_slug = self.blog.slug
        year = self.display_time.year
        month = self.display_time.month
        day = self.display_time.day

        return ("apps.blog.views.blog_entry", (),
                dict(blog_slug=blog_slug, year=year, month=month, day=day, slug=self.slug))
