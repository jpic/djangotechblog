import models
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404

from techblog import broadcast

from django.conf import settings


@broadcast.recieve()
def allow_comment(object):
    if isinstance(object, models.Page):
        return True
    return False

@broadcast.recieve()
def new_comment(object, comment):
    comment.moderated = True
    comment.visible = True


def page(request, path):

    page = get_object_or_404(models.Page, path=path)

    sections = page.get_sections()


    td = dict( page=page,
               sections=sections,
               )

    return render_to_response(page.get_template_names(), td)