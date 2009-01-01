# Create your views here.
import models
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.core.paginator import Paginator
from django.conf import settings
import urllib

from datetime import datetime, timedelta
import tools
from techblog import broadcast
from techblog.markup.extendedmarkup import combine_sections

from itertools import groupby


@broadcast.recieve()
def allow_comment(object):
    if isinstance(object, models.Post):
        return True
    return False

@broadcast.recieve()
def new_comment(object, comment):
    comment.moderated = True
    comment.visible = True


def get_channel_or_blog(slug):
    try:
        return models.Channel.objects.get(slug=slug)
    except models.Channel.DoesNotExist:
        return get_object_or_404(models.Blog, slug=slug)


def get_blog_list_data(request, posts, get_page_url, page_no):


    paginator = Paginator(posts, 10)

    if page_no > paginator.num_pages:
        raise Http404

    page = paginator.page(page_no)
    posts = page.object_list

    num_pages = paginator.num_pages

    newer_page_url = get_page_url(page_no - 1, num_pages)
    older_page_url = get_page_url(page_no + 1, num_pages)


    td = dict(page = page,
              page_no = page_no,
              posts = posts,
              older_page_url = older_page_url,
              newer_page_url = newer_page_url)

    return td



def blog_month(request, blog_slug, year, month, page_no=1):

    page_no = int(page_no)
    #if page_no < 1:
    #    raise Http404
    #if month < 1 or month > 12:
    #    raise Http404

    year = int(year)
    month = int(month)

    blog = get_channel_or_blog(blog_slug)

    start_date = datetime(year, month, 1)
    year_end = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        year_end += 1
    end_date = datetime(year_end, next_month, 1)

    title = blog.title


    posts = blog.posts().filter(display_time__gte=start_date, display_time__lt=end_date)
    archives = tools.collate_archives(blog)

    def get_page_url(page_no, num_pages):
        if page_no < 1 or page_no > num_pages:
            return ""
        if page_no == 1:
            return reverse("blog_month", kwargs = dict(blog_slug=blog_slug, year=year, month=month))
        else:
            return reverse("blog_month_with_page", kwargs = dict(blog_slug=blog_slug, year=year, month=month, page_no=page_no))


    td = get_blog_list_data(request, posts, get_page_url, page_no)

    sections = blog.description_data.get('sections', None)

    td.update(  dict(blog = blog,
                sections = sections,
                title = title,
                page_title = title,
                tagline = blog.tagline,
                archives = archives,
                month = month,
                year = year) )

    return render_to_response(blog.get_template_names("blog/month.html"), td)


def blog_front(request, blog_slug, page_no=1):

    page_no = int(page_no)
    if page_no < 1:
        raise Http404

    blog = get_channel_or_blog(blog_slug)

    title = blog.title
    posts = blog.posts()

    archives = tools.collate_archives(blog)

    def get_page_url(page_no, num_pages):
        if page_no < 1 or page_no > num_pages:
            return ""
        if page_no == 1:
            return reverse("blog_front", kwargs={"blog_slug":blog_slug})
        else:
            return reverse("blog_front_with_page", kwargs={"blog_slug":blog_slug, "page_no":str(page_no)})

    td = get_blog_list_data(request, posts, get_page_url, page_no)

    sections = blog.description_data.get('sections', None)

    feeds = [blog.get_feed()]

    td.update(  dict(   blog = blog,
                        title = title,
                        page_title = title,
                        tagline = blog.tagline,
                        archives = archives,
                        sections = sections,
                        feeds = feeds) )

    return render_to_response(blog.get_template_names("blog/index.html"), td)



def get_related_posts(blog, post, count=10):


    tags = list(post.tags.all())

    posts = models.Post.objects.filter(blog=blog, tags__in=tags).exclude(pk=post.id).order_by('-display_time')[:1000]

    def count_iter(i):
        return sum(1 for _ in i)

    counts_and_posts = [(post, count_iter(similar_posts)) for post, similar_posts in groupby(posts)]
    counts_and_posts.sort(key=lambda i:(i[1], i[0].display_time))
    return [cp[0] for cp in reversed(counts_and_posts[-count:])]

    #return posts


def blog_post(request, blog_slug, year, month, day, slug):

    blog = get_channel_or_blog(slug=blog_slug)

    year = int(year)
    month = int(month)
    day = int(day)

    post_day_start = datetime(year, month, day)
    post_day_end = post_day_start + timedelta(days=1)

    if post_day_start > datetime.now():
        raise Http404

    post = get_object_or_404(models.Post,
                             display_time__gte=post_day_start,
                             display_time__lt=post_day_end,
                             slug=slug,
                             blog__slug=blog_slug,
                             published=True)

    sections = combine_sections( blog.description_data.get('sections', None),
                                 post.content_data.get('sections', None) )


    prev_post = None
    next_post = None
    try:
        prev_post = models.Post.objects.filter(blog=blog, display_time__lt=post.display_time).order_by('-display_time')[0]
    except IndexError:
        pass

    try:
        next_post = models.Post.objects.filter(blog=blog, display_time__gt=post.display_time).order_by('display_time')[0]
    except IndexError:
        pass

    tags = list(post.tags.all().order_by('slug'))
    #tags.sort(key = lambda t:t.name.lower())


    related_posts = get_related_posts(blog, post)

    td = dict(  blog=blog,
                year=year,
                month=month,
                day=day,
                post=post,
                prev_post=prev_post,
                next_post=next_post,
                page_title = post.title,
                tagline = post.blog.title,
                tags = tags,
                related_posts = related_posts,
                sections = sections)

    return render_to_response(blog.get_template_names("blog/entry.html"), td)




def tag(request, blog_slug, tag_slug, page_no=1):

    page_no = int(page_no)
    if page_no < 1:
        raise Http404

    blog = get_channel_or_blog(blog_slug)
    tag = get_object_or_404(models.Tag, slug=tag_slug)

    title = blog.title
    posts = tag.posts()


    paginator = Paginator(posts, 5)

    if page_no > paginator.num_pages:
        raise Http404

    page = paginator.page(page_no)
    posts = page.object_list

    archives = tools.collate_archives(blog)

    def get_page_url(page_no):
        if page_no < 1 or page_no > paginator.num_pages:
            return ""
        if page_no == 1:
            return reverse("blog_tag", kwargs=dict(blog_slug=blog_slug, tag_slug=tag_slug))
        else:
            return reverse("blog_tag_with_page", kwargs=dict(blog_slug=blog_slug, tag_slug=tag_slug, page_no=page_no))

    newer_page_url = get_page_url(page_no - 1)
    older_page_url = get_page_url(page_no + 1)

    sections = combine_sections( blog.description_data.get('sections', None),
                                 tag.description_data.get('sections', None) )

    feeds = [tag.get_feed()]

    td = dict(blog = blog,
              tag = tag,
              title = title,
              page_title = title,
              tagline = blog.tagline,
              archives = archives,
              page = page,
              page_no = page_no,
              posts = posts,
              sections = sections,
              older_page_url = older_page_url,
              newer_page_url = newer_page_url,
              feeds = feeds)

    return render_to_response("blog/tag.html", td)

from techblog.markup.render import render_comment

def xhr_preview_comment(request):

    #if settings.DEBUG:
    #    import time
    #    time.sleep(3)

    bbcode = request.REQUEST.get('bbcode', '')
    html, summary, text, data = render_comment(bbcode, 'comment_bbcode')

    comment = {}
    comment['content_html'] = html
    comment['url'] = request.REQUEST.get('url')
    comment['name'] = request.REQUEST.get('name')
    comment['email'] = request.REQUEST.get('email')
    comment['created_time'] = datetime.now()

    td = {}
    td['comment'] = comment

#    import time
#    time.sleep(3);

    return render_to_response("xhr_comment_preview.html", td)


def import_wxr(request):

    from forms import ImportForm

    if request.method == "POST":

        form = ImportForm(request.POST, request.FILES)

        if form.is_valid():

            if form.cleaned_data.get('format') == "WXR":

                blog_slug = form.cleaned_data['blog_slug']
                wxr_file = request.FILES['input_file']
                tools.import_wxr(blog_slug, wxr_file)
    else:

        form = ImportForm()

    td = dict(form=form)


    return render_to_response("blog/tools/import_wxr.html", td)


def front(request):
    template_data = {}
    return render_to_response("blog_base.html", template_data)
