from models import Comment
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

from techblog import broadcast
from forms import CommentForm

import simplejson

def xhr_post_comment(request):

    if settings.DEBUG:
        import time
        time.sleep(3)

    errors = []

    form = CommentForm(request.POST)

    response = {'status': 'ok', 'errors' : []}
    if not form.is_valid():
        response['status'] = "fail"
        response['errors'] = dict((str(key), str(value)) for key, value in form.errors.iteritems())
    else:
        name = form.cleaned_data.get('name', '');
        email = form.cleaned_data.get('email', '')
        url = form.cleaned_data.get('url', '')
        content = form.cleaned_data.get('content', '')
        content_format = form.cleaned_data.get('content_format', '')

        content_type = form.cleaned_data.get('content_type')
        object_id = int(form.cleaned_data.get('object_id'))

        app_label, model = content_type.split('.')

        ct = ContentType.objects.get(app_label=app_label, model=model)
        object = ct.get_object_for_this_type(id=object_id)

        if not broadcast.first.allow_comment(object):

            response['status'] = "fail"
            response['errors'].append('Commenting not permited on this object')

        else:

            comment = Comment(
                content_type = ct,
                content_object = object,
                name = name,
                email = email,
                url = url
            )
            comment.content_markup_type
            comment.content = content

            broadcast.call.new_comment(object, comment)

            comment.save()
            response['comment_id'] = comment.id

    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')
