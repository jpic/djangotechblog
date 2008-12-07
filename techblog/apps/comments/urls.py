import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url('^xhr/post/$', views.xhr_post_comment, name='xhr_post_comment'),
                       )
