#!/usr/bin/env python
import postmarkup
import markuptags

MARKUP_TYPES = [ ("html", "Raw HTML"),
                ("postmarkup", "Postmarkup (BBCode like)"),
                ]

post_markup = postmarkup.create()
post_markup.add_tag(markuptags.PyTag, "py")
post_markup.add_tag(markuptags.EvalTag, "eval")
post_markup.add_tag(markuptags.HTMLTag, "html")


def render_post_markup(model):

    if model.markup_type == "html":

        model.html = model.markup_raw
        model.text = postmarkup.textilize(model.html)
        model.data = {}

    elif model.markup_type =="postmarkup":

        tag_data = {}
        html = post_markup( model.markup_raw,
                            paragraphs=True,
                            clean=True,
                            tag_data=tag_data )

        model.html = html
        model.text = postmarkup.textilize(html)
        model.data = tag_data.get('output', {})
