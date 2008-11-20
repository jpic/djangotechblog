# Create your views here.
import models
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from datetime import datetime, timedelta
import tools


def blog_front(request, blog_slug, page=1):

    blog = get_object_or_404(models.Blog, slug=blog_slug)

    title = blog.title

    posts = blog.posts()
    entries = posts
    entries_count = posts.count()

    start_index = (page-1) * blog.posts_per_page
    last_index = start_index + blog.posts_per_page

    entries = entries[start_index:last_index+1]

    archives = tools.collate_archives(blog)

    #if not entries:
    #    raise Http404

    td = dict(blog = blog,
              title = title,
              page_title = title,
              tagline = blog.tagline,
              entries = entries,
              archives = archives)


    return render_to_response("blog.html", td)


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

    td = dict(  blog=blog,
                year=year,
                month=month,
                day=day,
                entry=entry,
                page_title = entry.title,
                tagline = entry.blog.title)

    return render_to_response("blog_entry.html", td)

def front(request):
    template_data = {}
    return render_to_response("blog_base.html", template_data)
