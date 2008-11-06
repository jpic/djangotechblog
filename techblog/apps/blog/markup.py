#!/usr/bin/env python
import postmarkup
import markuptags

VERSION = 1

MARKUP_TYPES = [ ("html", "Raw HTML"),
                ("postmarkup", "Postmarkup (BBCode like)"),
                ]

post_markup = postmarkup.create()
post_markup.add_tag(markuptags.PyTag, "py")
post_markup.add_tag(markuptags.EvalTag, "eval")
post_markup.add_tag(markuptags.HTMLTag, "html")
post_markup.add_tag(postmarkup.SectionTag, "in")
post_markup.add_tag(markuptags.SummaryTag, "summary")


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

        print repr(model.markup_raw)
        model.html = html
        model.text = postmarkup.textilize(html)
        output = tag_data.get('output', {})
        sections = output.get("sections", {})
        for key, value in sections.items():
            sections[key] = [post_markup(s, paragraphs=True, clean=True) for s in value]
        model.data = output

        summary_markup = output.get("summary", "")
        if summary_markup.strip():
            summary = post_markup(output.get("summary" , ""), paragraphs=True, clean=True)
            model.summary_html = summary