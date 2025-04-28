import re


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

        # Properly escape HTML entities in code content
        escaped_content = (
            code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

        placeholder = f"CODEBLOCKPLACEHOLDER{len(placeholders)}"
        placeholders.append(placeholder)
        if not language:
            html_code_block = f"<pre><code>{escaped_content}</code></pre>"
        else:
            html_code_block = (
                f'<pre><code class="language-{language}">{escaped_content}</code></pre>'
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
