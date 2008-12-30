import models
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404

from techblog import broadcast

from django.conf import settings


def page(request, page_url):
    
    path = page_url.split('/')