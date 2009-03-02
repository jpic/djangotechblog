from django.core.cache import cache
import urlparse
from django.conf import settings

def clear_cached_page(path):

    url_key = urlparse.urlsplit(path)[2]
    key_prefix = getattr(settings, 'CACHE_MIDDLEWARE_KEY_PREFIX', '')
    cache_key = "views.decorators.cache.cache_header.%s.%s" % (key_prefix, url_key)
    cache.delete(cache_key)
