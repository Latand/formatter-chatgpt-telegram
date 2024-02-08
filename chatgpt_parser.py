import re


def ensure_closing_delimiters(text: str):
    """
    Ensures that if an opening ` or ``` is found without a matching closing delimiter,
    the missing delimiter is appended to the end of the text.
    """
    # For triple backticks
    if text.count("```") % 2 != 0:
        text += "```"
    # For single backticks
    if text.count("`") % 2 != 0:
        text += "`"
    return text


def extract_and_convert_code_blocks(text: str):
    """
    Extracts code blocks from the text, converting them to HTML <pre><code> format,
    and replaces them with placeholders. Also ensures closing delimiters for unmatched blocks.
    """
    text = ensure_closing_delimiters(text)
    placeholders = []
    code_blocks = {}

    def replacer(match):
        language = match.group(1) if match.group(1) else ""
        code_content = match.group(3)
        placeholder = f"CODEBLOCKPLACEHOLDER{len(placeholders)}"
        placeholders.append(placeholder)
        if not language:
            html_code_block = f"<pre><code>{code_content}</code></pre>"
        else:
            html_code_block = (
                f'<pre><code class="language-{language}">{code_content}</code></pre>'
            )
        return (placeholder, html_code_block)

    modified_text = text
    for match in re.finditer(r"```(\w*)?(\n)?(.*?)```", text, flags=re.DOTALL):
        placeholder, html_code_block = replacer(match)
        code_blocks[placeholder] = html_code_block
        modified_text = modified_text.replace(match.group(0), placeholder, 1)

    return modified_text, code_blocks


def reinsert_code_blocks(text: str, code_blocks: dict):
    """
    Reinserts HTML code blocks into the text, replacing their placeholders.
    """
    for placeholder, html_code_block in code_blocks.items():
        text = text.replace(placeholder, html_code_block, 1)
    return text


def split_by_tag(out_text: str, md_tag: str, html_tag: str) -> str:
    """
    Splits the text by markdown tag and replaces it with the specified HTML tag.
    """
    tag_pattern = re.compile(
        r"{}(.*?){}".format(re.escape(md_tag), re.escape(md_tag)), re.DOTALL
    )
    return tag_pattern.sub(r"<{}>\1</{}>".format(html_tag, html_tag), out_text)


def telegram_format(text: str) -> str:
    """
    Converts markdown in the provided text to HTML supported by Telegram.
    """

    # Step 1: Extract and convert code blocks first
    output, code_blocks = extract_and_convert_code_blocks(text)

    # Step 2: Escape HTML special characters in the output text
    output = output.replace("<", "&lt;").replace(">", "&gt;")

    # Inline code
    output = re.sub(r"`(.*?)`", r"<code>\1</code>", output)

    # Nested Bold and Italic
    output = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", output)

    # Process markdown formatting tags (bold, underline, italic, strikethrough)
    # and convert them to their respective HTML tags
    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "_", "i")
    output = split_by_tag(output, "*", "i")
    output = split_by_tag(output, "~~", "s")
    output = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', output)  # Links
    output = re.sub(r"^\s*[\-\*] (.+)", r"• \1", output, flags=re.MULTILINE)  # Lists

    output = re.sub(r"^\s*#+ (.+)", r"<b>\1</b>", output, flags=re.MULTILINE)

    # Step 4: Reinsert the converted HTML code blocks
    output = reinsert_code_blocks(output, code_blocks)
    return output
