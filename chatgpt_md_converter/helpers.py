def remove_blockquote_escaping(output: str) -> str:
    """
    Removes the escaping from blockquote tags.
    """
    output = output.replace("&lt;blockquote&gt;", "<blockquote>").replace(
        "&lt;/blockquote&gt;", "</blockquote>"
    )
    return output
