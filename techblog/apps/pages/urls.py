import views
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns =  patterns('',
                url(r'^(?P<path>.*)$', views.page, name="page"),
                )