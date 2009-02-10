import models
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.contrib.auth.decorators import *
from django.template.context import RequestContext

from techblog import broadcast
import forms

from django.conf import settings


@broadcast.recieve()
def allow_comment(object):
    if isinstance(object, models.Page):
        return True
    return False

@broadcast.recieve()
def new_comment(object, comment):
    if isinstance(object, models.Page):
        comment.moderated = True
        comment.visible = True
    else:
        raise broadcast.RejectBroadcast


def page(request, path):

    page = get_object_or_404(models.Page, path=path, version='live')

    is_preview = False
    if 'version' in request.GET and not request.user.is_anonymous():
        version = request.GET.get('version')
        if not page.version_exists(version):
            raise Http404
        page = page.get_version(version)
        is_preview = True

    sections = page.get_sections()


    td = dict( page=page,
               sections=sections,
               )

    return render_to_response(page.get_template_names(), td)


@login_required
def writer(request, page_id):

    page = get_object_or_404(models.Page, id=page_id, version='live')

    edit_page = page

    if page.version_exists('draft'):
        page = post.get_version('draft')

    page_slug = page.slug
    if '|' in page_slug:
        page_slug = page_slug.split('|', 1)[-1]

    auto_url = ''

    def save_to(save_page):
        a=request.POST.get

        save_page.title = a('title', save_post.title)
        save_page.slug = a('slug', save_post.slug)
        if not save_page.slug.strip():
            save_page.slug = slugify(save_page.title)
        save_page.inherit = a('inherit', save_page.inherit) == 'on'
        save_page.promoted = a('promoted', save_page.promoted) == 'on'
        save_page.promoted = a('published', save_page.published) == 'on'
        save_page.content = a('content', save_page.content)
        save_page.save()

    if request.method == "page":

        if 'save' in request.POST:

            draft_post = edit_post.get_version('draft')
            save_to(draft_post)
            post = draft_post
            edit_post.delete_version('preview')

        elif 'revert' in request.POST:

            edit_post.delete_version('draft')
            edit_post.delete_version('preview')
            post = edit_post
            #draft_post = edit_post.get_version('draft')
            #post = draft_post

        elif 'publish' in request.POST:

            save_to(edit_post)
            post_url = reverse('blog_post', args=(blog.slug, edit_post.display_time.year, edit_post.display_time.month, edit_post.display_time.day, edit_post.slug))
            edit_post.delete_version('preview')
            edit_post.delete_version('draft')
            post = edit_post
            post.published = True
            post.save()
            return HttpResponseRedirect(post_url)

        elif 'preview' in request.POST:

            preview_post = edit_post.get_version('preview')
            save_to(preview_post)
            post_url = reverse('blog_post', args=(blog.slug, edit_post.display_time.year, edit_post.display_time.month, edit_post.display_time.day, edit_post.slug))
            auto_url = post_url + "?version=preview"
            post = preview_post

        form = forms.WriterForm()

    else:

        form = forms.WriterForm()

    td = dict(  page_slug=page_slug,
                page=page,
                auto_url=auto_url,
                edit_page=edit_page,
                form=form)

    return render_to_response("page/write.html",
                              td,
                              context_instance=RequestContext(request))