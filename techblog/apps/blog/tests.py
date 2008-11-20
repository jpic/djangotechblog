#!/usr/bin/env python
import models
from random import randint, sample, choice
from datetime import datetime, timedelta

text = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Cras non tortor. Sed nunc. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Duis vitae eros. Phasellus dui nisl, porta sed, tristique non, feugiat eu, metus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Duis tincidunt est sit amet quam. Praesent lacus mauris, lacinia vitae, suscipit ac, dignissim ut, massa. Sed rutrum, magna consectetuer sollicitudin auctor, urna tortor suscipit dolor, ac suscipit dui eros gravida erat. Morbi molestie, ligula vitae sagittis adipiscing, felis risus laoreet metus, nec accumsan sem libero ut elit. Pellentesque augue nibh, sollicitudin eu, porttitor sit amet, ultricies quis, odio. Nam id est. Nunc libero urna, hendrerit ut, suscipit et, mollis id, mi. Praesent lobortis leo at neque. Vivamus mattis aliquet ligula. Duis dui sem, posuere eu, porta ac, hendrerit et, ante. Nulla porttitor magna vel ante pharetra viverra. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin consequat tellus nec arcu. Phasellus auctor diam sit amet sapien"""

def create_blog(title="Test Blog", num_posts = 100):

    def paragraphs(count):
        return "\n".join("%s"% text for _ in xrange(count))

    def slugify(title):
        return title.lower().replace(' ', '_')

    blog = models.Blog(title = title,
                description = paragraphs(1),
                slug = slugify(title) )

    blog.save()

    words = """"random python I You like code life universe everything god"""
    """atheism hot very difficult easy hard dynamic of the in is under on through"""
    """extremely strangely hardly plainly transparently incredibly"""

    words = words.split()
    def random_title():
        num_words = randint(2,8)
        title = " ".join(sample(words, num_words))
        title += choice("!? ")
        return title.strip().title()

    display_time = datetime.now()
    for _ in xrange(num_posts):

        display_time -= timedelta(days = randint(2, 15))

        title = random_title()
        post = models.Post(    blog=blog,
                                published=True,
                                created_time = display_time,
                                display_time = display_time,
                                edit_time = display_time,
                                title = title,
                                slug=slugify(title),
                                content = paragraphs(randint(1,8)) )
        post.save()

    return blog