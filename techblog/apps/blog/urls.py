import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url('^(?P<blog_slug>.*)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>.*)/$', views.blog_entry, name="blog_entry"),
    url('^(?P<blog_slug>.*)/$', views.blog_front, name="blog_front"),
    url('^(?P<blog_slug>.*)/page/(?P<page>\d+)$', views.blog_front, name="blog_front_with_page"),

    )