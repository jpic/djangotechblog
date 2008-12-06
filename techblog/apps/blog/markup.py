#!/usr/bin/env python
import postmarkup
import markuptags
from fields import PickledObjectField, MarkupField

from markuprender import *

VERSION = 1


def render_post_markup(markup, markup_type):

    if markup_type =="postmarkup":

        tag_data = {}
        html = post_markup( markup,
                            paragraphs=True,
                            clean=True,
                            tag_data=tag_data )


        text = postmarkup.textilize(html)
        output = tag_data.get('output', {})
        sections = output.get("sections", {})
        for key, value in sections.items():
            sections[key] = [post_markup(s, paragraphs=True, clean=True) for s in value]
        data = output

        summary_markup = output.get("summary", "")
        summary_html = ""
        if summary_markup.strip():
            summary = post_markup(output.get("summary" , ""), paragraphs=True, clean=True)
            summary_html = summary
    else:

        html = markup
        summary_html = html
        text = postmarkup.textilize(html)
        data = {}

    return html, summary_html, text, data