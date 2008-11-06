# Create your views here.
import models
from django.shortcuts import get_object_or_404, render_to_response
from datetime import datetime

def blog_entry(request, blog_slug, year, month, day, slug):

    blog = get_object_or_404(models.Blog, slug=blog_slug)

    year = int(year)
    month = int(month)
    day = int(day)

    post_date = datetime(year, month, day)
    post = get_object_or_404(models.Post, display_time=post_date, slug=slug)

    template_data = dict(blog=blog,
                         year=year,
                         month=month,
                         day=day,
                         post_date=post_date,
                         post=post)

def front(request):
    template_data = {}
    return render_to_response("blog_base.html", template_data)
