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

    @models.permalink
    def get_absolute_url(self):
        return ("apps.blog.views.tag", (),
                dict(blog_slug=self.blog.slug, tag_slug=self.slug))



class Channel(models.Model):

    title = models.CharField("Channel Title", max_length=100)
    tagline = models.CharField("Tag line", max_length=200)
    slug = models.SlugField()

    description = markup.MarkupField(default="", renderer=markup.render_post_markup)

    blogs = models.ManyToManyField("Blog")


class TagCloud(object):

    def __init__(self, blog, max_tags = 50):

        self.blog = blog

        self.tags = list( Tag.objects.filter(blog=blog).order_by("-count") )
        if max_tags is not None:
            self.tags = self.tags[:max_tags]

        self.min_font = 8.0
        self.max_font = 22.0

    def set_scale(min_font, max_font):

        self.min_font = min_font
        self.max_font = max_font

    def __iter__(self):

        tag_counts = [tag.count for tag in self.tags]

        sorted_counts = sorted(list(set(tag_counts)))
        # tag_counts = [sorted_counts.index(count) for count in tag_counts]

        places = [sorted_counts.index(tag.count) for tag in self.tags]

        max_count = max(places)
        min_count = min(places)
        count_range = float(max_count - min_count)

        font_size_range = self.max_font - self.min_font

        tag_cloud = []
        for place, tag in zip(places, self.tags):
            if count_range:
                tag_scale = (place - min_count) / count_range
            else:
                tag_scale = .25

            font_size = int(round(self.min_font + tag_scale * font_size_range))

            tag_cloud.append( (tag_scale, font_size, tag) )

        tag_cloud = tag_cloud[::2][::-1] + tag_cloud[1::2]
        #tag_cloud = tag_cloud[::-1]

        for size_tag in tag_cloud:
            yield size_tag


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

    def get_tag_cloud(self, tag_count=50):

        return TagCloud(self)


        tags = list( Tag.objects.filter(blog=self).order_by("-count") )
        if tag_count is not None:
            tags = tags[:tag_count]

        tag_counts = [tag.count for tag in tags]
        max_count = max(tag_counts)
        min_count = min(tag_counts)
        count_range = float(max_count - min_count)

        tag_cloud = []
        for tag in tags:
            tag_scale = (tag.count - min_count) / count_range
            tag_scale = int(tag_scale * 10.0) + 1
            tag_cloud.append( (tag_scale, tag) )

        tag_cloud = tag_cloud[::2][::-1] + tag_cloud[1::2]

        return tag_cloud

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

    def get_summary(self):
        if self.content_summary_html:
            return self.content_summary_html
        else:
            return self.content_html

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

    def _remove_tags(self):

        if self.pk is not None:
            tags = Tag.objects.filter(blog=self.blog, post=self)
            for tag in self.tags.all():
                if not tag.decrement():
                    tag.delete()
                else:
                    tag.save()
                self.tags.remove(tag)


    def _add_tags(self):

        """Creates tags or increments tag counts as neccesary.

        """

        tags = [t.strip() for t in self.tags_text.split(',')]
        tags = list(set(tags))

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

        self._remove_tags()
        super(Post, self).save(*args, **kwargs)
        self._add_tags()
