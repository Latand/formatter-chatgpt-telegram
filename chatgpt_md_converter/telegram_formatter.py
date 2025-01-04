import re

from .converters import convert_html_chars, split_by_tag
from .extractors import extract_and_convert_code_blocks, reinsert_code_blocks
from .formatters import \
    combine_blockquotes  # fix_asterisk_equations is no longer used
from .helpers import remove_blockquote_escaping


def telegram_format(text: str) -> str:
    """
    Converts markdown in the provided text to HTML supported by Telegram.
    """

    # Step 0: Combine blockquotes
    text = combine_blockquotes(text)

    # Step 1: Convert HTML reserved symbols
    text = convert_html_chars(text)

    # Step 2: Extract and convert code blocks first
    output, code_blocks = extract_and_convert_code_blocks(text)

    # (REMOVED) Step 2.1: We no longer fix asterisk equations, so skip fix_asterisk_equations

    # Step 3: Escape HTML special characters in the output text
    output = output.replace("<", "&lt;").replace(">", "&gt;")

    # Convert headings (H1-H6)
    output = re.sub(r"^(#{1,6})\s+(.+)$", r"<b>\2</b>", output, flags=re.MULTILINE)

    # Convert unordered lists (do this before italic detection so that leading '*' is recognized as bullet)
    output = re.sub(r"^(\s*)[\-\*]\s+(.+)$", r"\1• \2", output, flags=re.MULTILINE)

    # Inline code
    output = re.sub(r"`(.*?)`", r"<code>\1</code>", output)

    # Nested Bold and Italic
    # ***some text*** => <b><i>...</i></b>
    output = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", output)
    # ___some text___ => <u><i>...</i></u>
    output = re.sub(r"\_\_\_(.*?)\_\_\_", r"<u><i>\1</i></u>", output)

    # Process markdown for bold (**), underline (__), strikethrough (~~)
    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "~~", "s")

    # Custom approach for single-asterisk italic:
    # Require that there's no alphanumeric before the asterisk,
    # and no whitespace immediately after it, to avoid matching equations like 2*x.
    italic_pattern = re.compile(
        r"(?<![A-Za-z0-9])\*(?=[^\s])(.*?)(?<!\s)\*(?![A-Za-z0-9])",
        re.DOTALL
    )
    output = italic_pattern.sub(r"<i>\1</i>", output)

    # Process single underscore-based italic
    output = split_by_tag(output, "_", "i")

    # Remove storage links (Vector storage placeholders like 【4:0†source】)
    output = re.sub(r"【[^】]+】", "", output)

    # Convert Markdown links/images to <a href="">…</a>
    link_pattern = r"(?:!?)\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)"
    output = re.sub(link_pattern, r'<a href="\2">\1</a>', output)

    # Step 4: Reinsert the converted HTML code blocks
    output = reinsert_code_blocks(output, code_blocks)

    # Step 5: Remove blockquote escaping
    output = remove_blockquote_escaping(output)

    # Clean up multiple consecutive newlines, but preserve intentional spacing
    output = re.sub(r"\n{3,}", "\n\n", output)

    return output.strip()
