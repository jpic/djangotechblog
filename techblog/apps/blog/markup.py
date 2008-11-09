#!/usr/bin/env python
import postmarkup
import markuptags
from fields import PickledObjectField
from django.db.models import CharField, TextField, IntegerField

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

class MarkupField(TextField):

    def __init__(self, renderer=None, *args, **kwargs):
        self._renderer_callback = renderer
        super(MarkupField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):

        self._html_field = name + "_html"
        self._type_field = name + "_type"
        self._version_field = name + "_version"
        self._summary_field = name + "_summary_html"
        self._text_field = name + "_text"
        self._data_field = name + "_data"

        CharField("Markup type", blank=False, max_length=20, choices=MARKUP_TYPES, default="postmarkup").contribute_to_class(cls, self._type_field)
        IntegerField(default=0).contribute_to_class(cls, self._version_field)
        TextField(editable=True, blank=True, default="").contribute_to_class(cls, self._html_field)
        TextField(editable=True, blank=True, default="").contribute_to_class(cls, self._summary_field)
        TextField(editable=False, blank=True, default="").contribute_to_class(cls, self._text_field)
        PickledObjectField(editable=False, default={}, blank=True).contribute_to_class(cls, self._data_field)

        super(MarkupField, self).contribute_to_class(cls, name)


    def pre_save(self, model_instance, add):

        markup = getattr(model_instance, self.attname)
        markup_type = getattr(model_instance, self._type_field)

        html, summary_html, text, data = self._renderer_callback(markup, markup_type)

        setattr(model_instance, self._html_field, html)
        setattr(model_instance, self._summary_field, summary_html)
        setattr(model_instance, self._text_field, text)
        setattr(model_instance, self._data_field, data)
        return markup


def render_post_markup(markup, markup_type):

    print markup_type, markup

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