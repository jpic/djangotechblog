from django import template
from django.template.defaultfilters import stringfilter
import re
from techblog.apps.blog import tools, models
from techblog.apps.comments.models import Comment

register = template.Library()


short_months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
long_months = "January February March April May June July August September October November December".split()

@register.filter
@stringfilter
def shortmonth(value):
    try:
        month_index = int(value)
    except ValueError:
        return "INVALID MONTH"

    return short_months[month_index-1]


@register.filter
@stringfilter
def longmonth(value):
    try:
        month_index = int(value)
    except ValueError:
        return "INVALID MONTH"

    return long_months[month_index-1]

_re_first_paragraph = re.compile(r"<p>.*?</p>")

@register.filter
@stringfilter
def first_paragraph(value):
    match = _re_first_paragraph.match(value)
    if not match:
        return value
    return match.group(0)


@register.filter
@stringfilter
def smart_title(value):
    def title(word):
        for c in word:
            if c.isupper():
                return word
        return word.title()
    return u" ".join(title(value) for value in value.split())


_re_archives_tag = re.compile(r'for (?P<object>\w+) as (?P<name>\w+)')

class GetArchivesNode(template.Node):
    def __init__(self, blog_name, value_name):
        self.blog_name = blog_name
        self.value_name = value_name

    def render(self, context):

        blog = context.get(self.blog_name, None)
        if object is None:
            return ''

        archives = tools.collate_archives(blog)

        context[self.value_name] = archives
        return ''

@register.tag
def get_archives(parser, token):

    directive = token.contents.strip().split(' ', 1)[1]

    match = _re_archives_tag.match(directive)

    if match is None:
        raise template.TemplateSyntaxError("Syntax error")

    blog_name = match.group(1)
    value_name = match.group(2)

    return GetArchivesNode(blog_name, value_name)


_re_tags_tag = re.compile(r'for (?P<object>\w+) as (?P<name>\w+) max (?P<count>\d+)')


class GetTagsNode(template.Node):
    def __init__(self, blog_name, value_name, max_count):
        self.blog_name = blog_name
        self.value_name = value_name
        self.max_count = max_count

    def render(self, context):

        blog = context.get(self.blog_name, None)
        if object is None:
            return ''

        tags = blog.get_tag_cloud(self.max_count)

        context[self.value_name] = tags
        return ''


@register.tag
def get_tags(parser, token):

    directive = token.contents.strip().split(' ', 1)[1]

    match = _re_tags_tag.match(directive)


    if match is None:
        raise template.TemplateSyntaxError("Syntax error")

    blog_name = match.group(1)
    value_name = match.group(2)
    try:
        max_count = int(match.group(3))
    except ValueError:
        raise template.TemplateSyntaxError("Max tag count should be an integer")

    return GetTagsNode(blog_name, value_name, max_count)



class GetRecentNode(template.Node):
    def __init__(self, blog_name, value_name, max_count):
        self.blog_name = blog_name
        self.value_name = value_name
        self.max_count = max_count

    def render(self, context):

        blog = context.get(self.blog_name, None)
        if object is None:
            return ''

        posts = blog.posts()[:self.max_count]

        context[self.value_name] = posts
        return ''


@register.tag
def get_recent_posts(parser, token):

    directive = token.contents.strip().split(' ', 1)[1]

    match = _re_tags_tag.match(directive)


    if match is None:
        raise template.TemplateSyntaxError("Syntax error")

    blog_name = match.group(1)
    value_name = match.group(2)
    try:
        max_count = int(match.group(3))
    except ValueError:
        raise template.TemplateSyntaxError("Max post count should be an integer")

    return GetRecentNode(blog_name, value_name, max_count)



class GetRecentCommentsNode(template.Node):
    def __init__(self, blog_name, value_name, max_count):
        self.blog_name = blog_name
        self.value_name = value_name
        self.max_count = max_count

    def render(self, context):

        blog = context.get(self.blog_name, None)
        if object is None:
            return ''

        if isinstance(blog, models.Channel):
            blogs = list(blog.blogs.all())
        else:
            blogs = [blog]

        groups = ["blog." + b.slug for b in blogs]
        comments = Comment.objects.filter_for_model(models.Post).filter(group__in=groups).order_by('-created_time')[:self.max_count]

        context[self.value_name] = comments

        return ''


@register.tag
def get_recent_comments(parser, token):

    directive = token.contents.strip().split(' ', 1)[1]

    match = _re_tags_tag.match(directive)

    if match is None:
        raise template.TemplateSyntaxError("Syntax error")

    blog_name = match.group(1)
    value_name = match.group(2)
    try:
        max_count = int(match.group(3))
    except ValueError:
        raise template.TemplateSyntaxError("Max post count should be an integer")

    return GetRecentCommentsNode(blog_name, value_name, max_count)
