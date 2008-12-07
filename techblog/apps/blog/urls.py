import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url('^xhr/preview_comment/$', views.xhr_preview_comment, name="xhr_preview_comment"),

    url('^(?P<blog_slug>[\w-]*)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]*)/$', views.blog_post, name="blog_post"),
    url('^(?P<blog_slug>[\w-]*)/(?P<year>\d+)/(?P<month>\d+)/$', views.blog_month, name="blog_month"),
    url('^(?P<blog_slug>[\w-]*)/(?P<year>\d+)/(?P<month>\d+)/page/(?P<page_no>\d+)/$', views.blog_month, name="blog_month_with_page"),

    url('^(?P<blog_slug>[\w-]*)/tag/(?P<tag_slug>[\w-]*)/$', views.tag, name="blog_tag"),
    url('^(?P<blog_slug>[\w-]*)/tag/(?P<tag_slug>[\w-]*)/page/(?P<page_no>\d+)/$', views.tag, name="blog_tag_with_page" ),

    url('^(?P<blog_slug>[\w-]*)/$', views.blog_front, name="blog_front"),
    url('^(?P<blog_slug>[\w-]*)/page/(?P<page_no>\d+)/$', views.blog_front, name="blog_front_with_page"),

    )