#!/usr/bin/env python
import postmarkup
from django.db import models
from fields import PickledObjectField

class Renderers():
    pass
renderers = Renderers()

renderers.blog = postmarkup.create()


def render_blogpost(markup, tag_data=None):
    return renderers.blog(markup, tag_data=tag_data, paragraphs=True, clean=True)
render_blogpost.version  = 1


def add_markup_to_model(model, name, description, renderer):

    name = name.lower()
    setattr(model, name+"_markup", models.TextField(description))
    setattr(model, name+"_version", models.IntegerField(description, default=0))
    setattr(model, name+"_html", models.TextField(description, default=0))
    setattr(model, name+"_data", PickledObjectField(description+" data"))

    def make_markup_getter(name, renderer):

        def get_markup(self):

            markup = getattr(self, name+"_markup")
            version = getattr(self, name+"_version")
            html = getattr(self, name+"_html")
            if version != renderer.version:
                tag_data = {}
                html = renderer(markup, tag_data=tag_data)
                setattr(self, name+"_data", tag_data)
                setattr(self, name+"_html", html)
            return html

    setattr(model, name, make_markup_getter(name, renderer) )
