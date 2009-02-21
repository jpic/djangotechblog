from django.contrib.sitemaps import Sitemap

from models import Post, Tag

from datetime import datetime, timedelta

class PostSitemap(Sitemap):
    
    def items(self):
        return Post.published_posts.all()

    def lastmod(self, obj):
        return max(obj.edit_time, obj.display_time)

    def changefreq(self, obj):

        now = datetime.now()
        t = obj.display_time
        days_since = (now - t).days

        if days_since < 1:
            return 'hourly'
        elif days_since < 7:
            return 'daily'
        elif days_since < 30:
            return 'weekly'
        elif days_since < 365:
            return 'monthly'
        else:
            return 'never'

    def priority(self):
        now = datetime.now()
        t = obj.display_time
        days_since = (now - t).days

        if days_since < 7:
            return 1.0
        elif days_since < 30:
            return .7
        else:
            return .5

    def location(self, obj):
        return obj.get_absolute_url()



class TagSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
