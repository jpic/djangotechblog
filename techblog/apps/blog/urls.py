import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url('^(?P<blog_slug>[\w-]*)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]*)/$', views.blog_entry, name="blog_entry"),

    url('^(?P<blog_slug>[\w-]*)/tag/(?P<tag_slug>[\w-]*)/$', views.tag, name="blog_tag"),
    url('^(?P<blog_slug>[\w-]*)/tag/(?P<tag_slug>[\w-]*)/(?P<page_no>\d+)/$', views.tag, name="blog_tag_with_page" ),

    url('^(?P<blog_slug>[\w-]*)/$', views.blog_front, name="blog_front"),
    url('^(?P<blog_slug>[\w-]*)/(?P<page_no>\d+)/$', views.blog_front, name="blog_front_with_page"),

    )