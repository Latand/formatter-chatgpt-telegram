import re


def convert_html_chars(text: str) -> str:
    """
    Converts HTML reserved symbols to their respective character references.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def split_by_tag(out_text: str, md_tag: str, html_tag: str) -> str:
    """
    Splits the text by markdown tag and replaces it with the specified HTML tag.
    """
    tag_pattern = re.compile(
        r"(?<!\w){}(.*?){}(?!\w)".format(re.escape(md_tag), re.escape(md_tag)),
        re.DOTALL,
    )
    return tag_pattern.sub(r"<{}>\1</{}>".format(html_tag, html_tag), out_text)
