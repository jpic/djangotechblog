# Create your views here.
import models
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.core.paginator import Paginator

from datetime import datetime, timedelta
import tools

from itertools import groupby

def blog_front(request, blog_slug, page=1):

    page = int(page)
    if page < 1:
        raise Http404

    blog = get_object_or_404(models.Blog, slug=blog_slug)

    title = blog.title

    posts = blog.posts()
    entries = posts
    entries_count = posts.count()
    total_pages = entries_count / blog.posts_per_page

    if page > total_pages:
        raise Http404

    start_index = (page-1) * blog.posts_per_page
    last_index = start_index + blog.posts_per_page

    entries = entries[start_index:last_index]

    archives = tools.collate_archives(blog)

    def get_page_url(page):
        if page < 1 or page > total_pages:
            return ""
        if page == 1:
            return reverse("blog_front", kwargs={"blog_slug":blog_slug})
        else:
            return reverse("blog_front_with_page", kwargs={"blog_slug":blog_slug, "page":str(page)})

    newer_page_url = get_page_url(page - 1)
    older_page_url = get_page_url(page + 1)


    td = dict(blog = blog,
              title = title,
              page_title = title,
              tagline = blog.tagline,
              entries = entries,
              archives = archives,
              page = page,
              older_page_url = older_page_url,
              newer_page_url = newer_page_url)


    return render_to_response("blog.html", td)


def get_related_posts(blog, post, count=10):


    tags = list(post.tags.all())

    posts = models.Post.objects.filter(blog=blog, tags__in=tags).exclude(pk=post.id).order_by('-display_time')[:1000]

    def count_iter(i):
        return sum(1 for _ in i)

    counts_and_posts = [(post, count_iter(similar_posts)) for post, similar_posts in groupby(posts)]
    counts_and_posts.sort(key=lambda i:(i[1], i[0].display_time))
    return [cp[0] for cp in reversed(counts_and_posts[-count:])]

    #return posts


def blog_entry(request, blog_slug, year, month, day, slug):

    blog = get_object_or_404(models.Blog, slug=blog_slug)

    year = int(year)
    month = int(month)
    day = int(day)

    post_day_start = datetime(year, month, day)
    post_day_end = post_day_start + timedelta(days=1)

    if post_day_start > datetime.now():
        raise Http404

    entry = get_object_or_404(models.Post,
                             display_time__gte=post_day_start,
                             display_time__lt=post_day_end,
                             slug=slug,
                             published=True)

    prev_entry = None
    next_entry = None
    try:
        prev_entry = models.Post.objects.filter(blog=blog, display_time__lt=entry.display_time).order_by('-display_time')[0]
    except IndexError:
        pass

    try:
        next_entry = models.Post.objects.filter(blog=blog, display_time__gt=entry.display_time).order_by('display_time')[0]
    except IndexError:
        pass

    tags = list(entry.tags.all().order_by('slug'))
    #tags.sort(key = lambda t:t.name.lower())


    related_posts = get_related_posts(blog, entry)

    td = dict(  blog=blog,
                year=year,
                month=month,
                day=day,
                entry=entry,
                prev_entry=prev_entry,
                next_entry=next_entry,
                page_title = entry.title,
                tagline = entry.blog.title,
                tags = tags,
                related_posts = related_posts)

    return render_to_response("blog_entry.html", td)

def tag(request, blog_slug, tag_slug):

    blog = get_object_or_404(models.Blog, slug=blog_slug)
    tag = get_object_or_404(models.Tag, slug=tag_slug)

    posts = tag.post_set.all().order_by('-display_time')

    post_paginator = Paginator(posts, 20)

    td = dict(blog = blog,
              tag = tag,
              posts = posts,
              post_paginator = post_paginator)

    return render_to_response("blog_tag.html", td)





def front(request):
    template_data = {}
    return render_to_response("blog_base.html", template_data)
