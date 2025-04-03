def remove_blockquote_escaping(output: str) -> str:
    """
    Removes the escaping from blockquote tags, including expandable blockquotes.
    """
    # Regular blockquotes
    output = output.replace("&lt;blockquote&gt;", "<blockquote>").replace(
        "&lt;/blockquote&gt;", "</blockquote>"
    )

    # Expandable blockquotes
    output = output.replace(
        "&lt;blockquote expandable&gt;", "<blockquote expandable>"
    ).replace("&lt;/blockquote&gt;", "</blockquote>")

    return output


def remove_spoiler_escaping(output: str) -> str:
    """
    Ensures spoiler tags are correctly formatted (rather than being escaped).
    """
    # Fix any incorrectly escaped spoiler tags
    output = output.replace(
        '&lt;span class="tg-spoiler"&gt;', '<span class="tg-spoiler">'
    )
    output = output.replace("&lt;/span&gt;", "</span>")
    return output
