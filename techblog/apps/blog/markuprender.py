#!/usr/bin/env python
import postmarkup
import markuptags

post_markup = postmarkup.create()
post_markup.add_tag(markuptags.PyTag, "py")
post_markup.add_tag(markuptags.EvalTag, "eval")
post_markup.add_tag(markuptags.HTMLTag, "html")
post_markup.add_tag(postmarkup.SectionTag, "in")
post_markup.add_tag(markuptags.SummaryTag, "summary")

if __name__ == "__main__":

    test = """[summary]
This is a [b]summary[/b]...
[/summary]
Article"""

    tag_data = {}
    html = post_markup(test, paragraphs=True, clean=True, tag_data=tag_data)
    print html
    from pprint import pprint
    pprint(tag_data)