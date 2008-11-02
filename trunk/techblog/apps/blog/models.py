from django.db import models
from django.contrib.auth.models import User

import markup


# Create your models here.


class Blog(models.Model):

    title = models.CharField("Title of the Blog", max_length=100)
    slug = models.SlugField()
    author = models.ForeignKey(User)

    created_time = models.DateTimeField(auto_now_add=True)
    posted_time = models.DateTimeField(auto_now_add=True)

markup.add_markup_to_model(Blog, "description", "Blog description markup", markup.render_blogpost)

print dir(Blog)

class Post(models.Model):

    title = models.CharField("Post Title", max_length=100)
    slug = models.SlugField()

    created_time = models.DateTimeField(auto_now_add=True)
    posted_time = models.DateTimeField(auto_now_add=True)

markup.add_markup_to_model(Post, "content", "Post content", markup.render_blogpost)