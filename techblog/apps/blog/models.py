from django.db import models
from django.contrib.auth.models import User
from fields import PickledObjectField
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
import datetime

import markup

#
#from django.db.models.signals import post_save
#
#
#def _process_tags_signal(sender, **kwargs):
#    sender.
#
#post_save.connect(process_tags, sender=Post)

class Tag(models.Model):

    blog = models.ForeignKey("Blog")
    name = models.CharField("Tag name", max_length=100)
    slug = models.SlugField()

    count = models.IntegerField(default=0, editable=False)

    def decrement(self):
        count = self.count
        if count:
            count -= 1
            self.count = count
        return count

    def increment(self):
        self.count += 1
        return self.count

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
    slug = models.SlugField(unique=True)
    posts_per_page = models.IntegerField(default=10)

    description = markup.MarkupField(default="", renderer=markup.render_post_markup)

    def __unicode__(self):
        return self.title

    def posts(self):
        now = datetime.datetime.now()
        posts = self.post_set.filter(published=True,
                                     display_time__lte=now).order_by("-display_time")
        return posts


    @models.permalink
    def get_absolute_url(self):

        blog_slug = self.slug

        return ("apps.blog.views.blog_front", (),
                dict(blog_slug=blog_slug))

class Post(models.Model):

    blog = models.ForeignKey(Blog)

    title = models.CharField("Post Title", max_length=100)
    slug = models.SlugField("Post Slug", unique=True)
    published = models.BooleanField("Published?", default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    display_time = models.DateTimeField("Post Time", default=datetime.datetime.now)

    tags = models.ManyToManyField("Tag", blank=True)
    tags_text = models.TextField("Comma separated tags", default="")

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

    def _process_tags(self):

        """Creates tags or increments tag counts as neccesary.

        """

        tags = [t.lower().strip() for t in self.tags_text.split(',')]

        for tag_name in tags:
            tag_slug = slugify(tag_name)
            if tag_slug:
                try:
                    tag = Tag.objects.get(slug=tag_slug)
                except Tag.DoesNotExist:
                    tag = Tag( blog = self.blog,
                               name = tag_name,
                               slug = tag_slug)

                tag.increment()
                tag.save()

                self.tags.add(tag)



    def save(self, *args, **kwargs):

        super(Post, self).save(*args, **kwargs)
        self._process_tags()
