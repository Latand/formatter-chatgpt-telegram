def combine_blockquotes(text: str) -> str:
    """
    Combines multiline blockquotes into a single blockquote while keeping the \n characters.
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
                    "<blockquote>" + "\n".join(blockquote_lines) + "</blockquote>"
                )
                blockquote_lines = []
                in_blockquote = False
            combined_lines.append(line)

    if in_blockquote:
        combined_lines.append(
            "<blockquote>" + "\n".join(blockquote_lines) + "</blockquote>"
        )

    return "\n".join(combined_lines)


def fix_asterisk_equations(text: str) -> str:
    """
    Replaces numeric expressions with '*' in them with '×'
    to avoid accidental italic formatting.
    e.g. '6*8' -> '6×8', '6 * 8' -> '6×8'
    """
    import re
    eq_pattern = re.compile(r'(\d+)\s*\*\s*(\d+)')
    return eq_pattern.sub(r'\1×\2', text)
