#!/usr/bin/env python
import models
from itertools import groupby

def collate_archives(blog):

    """Groups the posts for a blog by month.

    blog -- A Blog model

    Returns a list of tuples containing the year (as an integer),
    the month (integer) and the number of posts in that month (integer).

    """

    posts = blog.post_set.all().values('display_time').order_by("-display_time")

    def count_iterable(i):
        return sum(1 for _ in i)

    def year_month(post):
        display_time = post['display_time']
        return (display_time.year, display_time.month)

    months = [(year, month, count_iterable(post_group)) for (year, month),post_group in groupby(posts, year_month)]

    years = [ (year,list(months)) for (year, months) in groupby(months, lambda m:m[0])]

    return years
