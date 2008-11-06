import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',

    ('^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>.*)/$', views.blog_entry),
    
    )