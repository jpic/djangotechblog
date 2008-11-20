#!/usr/bin/env python
import postmarkup
import markuptags

post_markup = postmarkup.create()
post_markup.add_tag(postmarkup.SectionTag, "in")


# Auto register markup tags...
for symbol in dir(markuptags):
    if symbol.startswith('__'):
        continue

    if symbol.endswith('Tag'):
        obj = getattr(markuptags, symbol)
        default_name = getattr(obj, 'DEFAULT_NAME', '')
        if default_name:
            post_markup.add_tag(obj, default_name)

#post_markup.add_tag(markuptags.PyTag, "py")
#post_markup.add_tag(markuptags.EvalTag, "eval")
#post_markup.add_tag(markuptags.HTMLTag, "html")
#post_markup.add_tag(markuptags.SummaryTag, "summary")
#post_markup.add_tag(markuptags.AnchorTag, "anchor")

if __name__ == "__main__":

    test = """[summary]
This is a [b]summary[/b]...[/summary]
Article [py]import postmarkup
print postmarkup.__version__[/py]
[eval safe]"<h1>Hello</h1>"[/eval]
Another paragraph"""

    tag_data = {}
    html = post_markup(test, paragraphs=True, clean=True, tag_data=tag_data)
    print html
    from pprint import pprint
    pprint(tag_data)