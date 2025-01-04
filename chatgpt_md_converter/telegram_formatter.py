import re

from .converters import convert_html_chars, split_by_tag
from .extractors import extract_and_convert_code_blocks, reinsert_code_blocks
from .formatters import combine_blockquotes
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

    # Step 3: Escape HTML special characters in the output text
    output = output.replace("<", "&lt;").replace(">", "&gt;")

    # Inline code
    output = re.sub(r"`(.*?)`", r"<code>\1</code>", output)

    # Nested Bold and Italic
    output = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", output)
    output = re.sub(r"\_\_\_(.*?)\_\_\_", r"<u><i>\1</i></u>", output)

    # Process markdown formatting tags (bold, underline, italic, strikethrough)
    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "_", "i")
    output = split_by_tag(output, "*", "i")
    output = split_by_tag(output, "~~", "s")

    # Remove storage links (Vector storage placeholders like 【4:0†source】)
    output = re.sub(r"【[^】]+】", "", output)

    # More precise pattern for capturing Markdown links and images
    # Handles nested brackets in link text and converts both links and images to <a> tags
    link_pattern = r"(?:!?)\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)"
    output = re.sub(link_pattern, r'<a href="\2">\1</a>', output)

    # Convert headings (H1-H6)
    output = re.sub(r"^(#{1,6})\s+(.+)$", r"<b>\2</b>", output, flags=re.MULTILINE)

    # Convert unordered lists
    output = re.sub(r"^(\s*)[\-\*]\s+(.+)$", r"\1• \2", output, flags=re.MULTILINE)

    # Step 4: Reinsert the converted HTML code blocks
    output = reinsert_code_blocks(output, code_blocks)

    # Step 5: Remove blockquote escaping
    output = remove_blockquote_escaping(output)

    # Clean up multiple consecutive newlines, but preserve intentional spacing
    output = re.sub(r"\n{3,}", "\n\n", output)

    return output.strip()
