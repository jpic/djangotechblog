#!/usr/bin/env python
from models import Blog, Post, Tag
from django.contrib.syndication.feeds import Feed
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.syndication.feeds import FeedDoesNotExist


class BlogFeed(Feed):

    @classmethod
    def get_url(self, blog):
        return reverse('blog_feeds', kwargs={'url':'blog/%s'%blog.slug})



    def get_object(self, bits):
        if len(bits) != 1:
            raise FeedDoesNotExist
        blog = Blog.objects.get(slug=bits[0])
        return blog

    def items(self, blog):
        return blog.posts()

    def title(self, blog):
        return blog.title

    def link(self, blog):
        if not blog:
            raise FeedDoesNotExist
        return blog.get_absolute_url()

    def description(self, blog):
        return mark_safe(blog.description_text)


    def item_pubdate(self, post):
        return post.display_time

class BlogTagFeed(Feed):

    @classmethod
    def get_url(self, tag):
        return reverse('blog_feeds', kwargs={'url':'tag/%s/%s'%(tag.blog.slug, tag.slug)})

    def get_object(self, bits):
        if len(bits) != 2:
            raise FeedDoesNotExist

        print bits
        blog_slug = bits[0]
        tag_slug = bits[1]

        tag = Tag.objects.get(blog__slug = blog_slug, slug=tag_slug)
        return tag

    def items(self, tag):
        return tag.posts()

    def title(self, tag):
        return "%s posts in '%s'" % (tag.name.title(), tag.blog.title)

    def link(self, tag):
        if not tag:
            raise FeedDoesNotExist
        return tag.get_absolute_url()

    def description(self, tag):
        return mark_safe(tag.description_text)

    def item_pubdate(self, post):
        return post.display_time


    #def item_author_name(self, post):
    #    return item.
