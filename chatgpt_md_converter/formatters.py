def combine_blockquotes(text: str) -> str:
    """
    Combines multiline blockquotes into a single blockquote while keeping the \n characters.
    Supports both regular blockquotes (>) and expandable blockquotes (**>).
    """
    lines = text.split("\n")
    combined_lines = []
    blockquote_lines = []
    in_blockquote = False
    is_expandable = False

    for line in lines:
        if line.startswith("**>"):
            # Expandable blockquote
            in_blockquote = True
            is_expandable = True
            blockquote_lines.append(line[3:].strip())
        elif line.startswith(">"):
            # Regular blockquote
            if not in_blockquote:
                # This is a new blockquote
                in_blockquote = True
                is_expandable = False
            blockquote_lines.append(line[1:].strip())
        else:
            if in_blockquote:
                # End of blockquote, combine the lines
                if is_expandable:
                    combined_lines.append(
                        "<blockquote expandable>"
                        + "\n".join(blockquote_lines)
                        + "</blockquote>"
                    )
                else:
                    combined_lines.append(
                        "<blockquote>" + "\n".join(blockquote_lines) + "</blockquote>"
                    )
                blockquote_lines = []
                in_blockquote = False
                is_expandable = False
            combined_lines.append(line)

    if in_blockquote:
        # Handle the case where the file ends with a blockquote
        if is_expandable:
            combined_lines.append(
                "<blockquote expandable>"
                + "\n".join(blockquote_lines)
                + "</blockquote>"
            )
        else:
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

    eq_pattern = re.compile(r"(\d+)\s*\*\s*(\d+)")
    return eq_pattern.sub(r"\1×\2", text)
