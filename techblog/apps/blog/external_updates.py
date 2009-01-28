from models import Microblog
from models import Post

from datetime import datetime
import twitter

from django.template.defaultfilters import slugify

def update():
    update_microblogs();

def update_microblogs():


    def char_break(text, num_chars):
        if len(text) < num_chars:
            return text
        return text[:num_chars-3].rsplit(' ', 1)[0] + '...'

    twitter_api = twitter.Api();
    for microblog in Microblog.objects.all():
        if not microblog.enabled:
            continue
        for tweet in twitter_api.GetUserTimeline(microblog.username):
            tweet_guid = u"TWITTER:%s" % str(tweet.id)
            try:
                post = Post.objects.get(blog=microblog.blog, guid=tweet_guid)
            except Post.DoesNotExist:
                tweet_time = datetime.fromtimestamp(tweet.created_at_in_seconds)
                title = char_break(tweet.text, 50)
                post = Post(blog = microblog.blog,
                            title = "Twitter: " + title,
                            tags_text = "twitter",
                            slug = slugify(title),
                            published = True,
                            guid = u"TWITTER:" + tweet_guid,
                            allow_comments=True,
                            created_time=datetime.now(),
                            edit_time=datetime.now(),
                            display_time=tweet_time,
                            content = tweet.text,
                            content_markup_type = "text",
                            version = 'live',
                            template_path = microblog.template_path,
                            )
                post.save()
