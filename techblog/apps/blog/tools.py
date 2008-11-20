#!/usr/bin/env python
import models
from itertools import groupby

def collate_posts(blog):

    """Groups the posts for a blog by month.

    blog -- A Blog model

    Returns a list of tuples containing the month (as an integer),
    the year (integer) and the number of posts in that month (integer).

    """

    posts = Blog.post_set.all().values('display_time').order_by("-display_time")

    def count_iterable(i):
        return sum(1 for _ in i)

    def month_year(post):
        display_time = post['display_time']
        return (display_time.month, display_time.year)

    months = [(date[0], date[1], count_iterable(post_group)) for date in groupby(posts, month_year)]

    return months
