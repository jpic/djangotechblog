import views
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns =  patterns('',
                url(r'^writer/(?P<page_id>\d+)/$', views.writer, name="pagewriter"),
                url(r'^newpage_/$', views.newpage, name="newpage"),
                url(r'^(?P<path>.*)/$', views.page, name="page"),
                )