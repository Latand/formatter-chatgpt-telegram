import re

from .converters import convert_html_chars, split_by_tag
from .extractors import extract_and_convert_code_blocks, reinsert_code_blocks
from .formatters import combine_blockquotes
from .helpers import remove_blockquote_escaping, remove_spoiler_escaping


def extract_inline_code_snippets(text: str):
    """
    Extracts inline code (single-backtick content) from the text,
    replacing it with placeholders, returning modified text and a dict of placeholders -> code text.
    This ensures characters like '*' or '_' inside inline code won't be interpreted as Markdown.
    """
    placeholders = []
    code_snippets = {}
    inline_code_pattern = re.compile(r"`([^`]+)`")

    def replacer(match):
        snippet = match.group(1)
        placeholder = f"INLINECODEPLACEHOLDER{len(placeholders)}"
        placeholders.append(placeholder)
        code_snippets[placeholder] = snippet
        return placeholder

    new_text = inline_code_pattern.sub(replacer, text)
    return new_text, code_snippets


def telegram_format(text: str) -> str:
    """
    Converts markdown in the provided text to HTML supported by Telegram.
    """

    # Step 0: Combine blockquotes
    text = combine_blockquotes(text)

    # Step 1: Extract and convert triple-backtick code blocks first
    output, triple_code_blocks = extract_and_convert_code_blocks(text)

    # Step 2: Extract inline code snippets
    output, inline_code_snippets = extract_inline_code_snippets(output)

    # Step 3: Convert HTML reserved symbols in the text (not in code blocks)
    output = convert_html_chars(output)

    # Convert headings (H1-H6)
    output = re.sub(r"^(#{1,6})\s+(.+)$", r"<b>\2</b>", output, flags=re.MULTILINE)

    # Convert unordered lists (do this before italic detection so that leading '*' is recognized as bullet)
    output = re.sub(r"^(\s*)[\-\*]\s+(.+)$", r"\1• \2", output, flags=re.MULTILINE)

    # Nested Bold and Italic
    output = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", output)
    output = re.sub(r"\_\_\_(.*?)\_\_\_", r"<u><i>\1</i></u>", output)

    # Process markdown for bold (**), underline (__), strikethrough (~~), and spoiler (||)
    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "~~", "s")
    output = split_by_tag(output, "||", 'span class="tg-spoiler"')

    # Custom approach for single-asterisk italic
    italic_pattern = re.compile(
        r"(?<![A-Za-z0-9])\*(?=[^\s])(.*?)(?<!\s)\*(?![A-Za-z0-9])", re.DOTALL
    )
    output = italic_pattern.sub(r"<i>\1</i>", output)

    # Process single underscore-based italic
    output = split_by_tag(output, "_", "i")

    # Remove storage links (Vector storage placeholders like 【4:0†source】)
    output = re.sub(r"【[^】]+】", "", output)

    # Convert Markdown links/images to <a href="">…</a>
    link_pattern = r"(?:!?)\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)"
    output = re.sub(link_pattern, r'<a href="\2">\1</a>', output)

    # Step 4: Reinsert inline code snippets, applying HTML escaping to the content
    for placeholder, snippet in inline_code_snippets.items():
        # Apply HTML escaping to the content of inline code
        escaped_snippet = (
            snippet.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        output = output.replace(placeholder, f"<code>{escaped_snippet}</code>")

    # Step 5: Reinsert the converted triple-backtick code blocks
    output = reinsert_code_blocks(output, triple_code_blocks)

    # Step 6: Remove blockquote escaping
    output = remove_blockquote_escaping(output)

    # Step 7: Remove spoiler tag escaping
    output = remove_spoiler_escaping(output)

    # Clean up multiple consecutive newlines, but preserve intentional spacing
    output = re.sub(r"\n{3,}", "\n\n", output)

    return output.strip()
