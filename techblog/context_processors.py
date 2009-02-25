#!/usr/bin/env python

from django.conf import settings

def google_analytics(request):
    return dict( GA_PATH = settings.GA_PATH )