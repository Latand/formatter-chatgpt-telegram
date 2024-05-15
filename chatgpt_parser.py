import re


def convert_html_chars(text: str) -> str:
    """
    Converts HTML reserved symbols to their respective character references.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def ensure_closing_delimiters(text: str) -> str:
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


def reinsert_code_blocks(text: str, code_blocks: dict) -> str:
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


def combine_blockquotes(text: str) -> str:
    """
    Combines multiline blockquotes into a single blockquote.
    """
    lines = text.split("\n")
    combined_lines = []
    blockquote_lines = []
    in_blockquote = False

    for line in lines:
        if line.startswith(">"):
            in_blockquote = True
            blockquote_lines.append(line[1:].strip())
        else:
            if in_blockquote:
                combined_lines.append(
                    "<blockquote>" + " ".join(blockquote_lines) + "</blockquote>"
                )
                blockquote_lines = []
                in_blockquote = False
            combined_lines.append(line)

    if in_blockquote:
        combined_lines.append(
            "<blockquote>" + " ".join(blockquote_lines) + "</blockquote>"
        )

    return "\n".join(combined_lines)


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

    # Process markdown formatting tags (bold, underline, italic, strikethrough)
    # and convert them to their respective HTML tags
    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "_", "i")
    output = split_by_tag(output, "*", "i")
    output = split_by_tag(output, "~~", "s")

    # Remove storage links
    output = re.sub(r"【[^】]+】", "", output)

    # Convert links
    output = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', output)

    # Convert lists
    output = re.sub(r"^\s*[\-\*] (.+)", r"• \1", output, flags=re.MULTILINE)

    # Convert headings
    output = re.sub(r"^\s*#+ (.+)", r"<b>\1</b>", output, flags=re.MULTILINE)

    # Step 4: Reinsert the converted HTML code blocks
    output = reinsert_code_blocks(output, code_blocks)

    # Step 5: Remove blockquote escaping
    output = output.replace("&lt;blockquote&gt;", "<blockquote>").replace(
        "&lt;/blockquote&gt;", "</blockquote>"
    )

    return output
