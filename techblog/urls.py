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

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}) )


urlpatterns += patterns('',
    (r'^blog/', include('apps.blog.urls')),
    (r'^comments/', include('apps.comments.urls')),
    (r'^pages/', include('apps.pages.urls')),
    #(r'^', include('apps.blog.urls'), {"blog_slug":"test-blog"}),
)
