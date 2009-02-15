from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    #url(r'^$', 'apps.blog.views.blog_front', {"blog_slug":"test-blog"}),
)


urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}) )


def bad(request):
    1/0

urlpatterns += patterns('',

    (r'^bad/$', bad),
    (r'^', include('techblog.apps.blog.urls'), {"blog_slug":settings.DEFAULT_BLOG_SLUG, "blog_root":"/"}),

    (r'^blog/(?P<blog_slug>[\w-]*)/', include('techblog.apps.blog.urls') ),

    (r'^comments/', include('techblog.apps.comments.urls')),
    (r'^pages/', include('techblog.apps.pages.urls')),
    (r'^accounts/', include('techblog.apps.accounts.urls'))

)
