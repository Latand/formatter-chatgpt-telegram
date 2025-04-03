# ChatGPT Markdown to Telegram HTML Parser

## Overview

This project provides a solution for converting Markdown formatted text into HTML markup supported by the Telegram Bot API, specifically tailored for use in ChatGPT bots developed with the OpenAI API. It includes features for handling various Markdown elements and ensures proper tag closure, making it suitable for streaming mode applications.

## Features

- Converts Markdown syntax to Telegram-compatible HTML.
- Supports inline code, bold, italic, underline, and strikethrough formatting.
- Supports spoiler tags with `||text||` syntax.
- Handles nested bold and italic formatting.
- Converts Markdown links and lists to their HTML equivalents.
- Processes code blocks with optional language specification, preserving formatting within `<pre><code>` tags.
- Supports regular blockquotes (`>`) and expandable blockquotes (`**>`) for Telegram.
- Automatically appends missing closing delimiters for code blocks.
- Escapes HTML special characters to prevent unwanted HTML rendering outside code blocks.

## Usage

To use the Markdown to Telegram HTML Parser in your ChatGPT bot, integrate the provided Python functions into your bot's processing pipeline. Here is a brief overview of how to incorporate the parser:

1. **Ensure Closing Delimiters**: Automatically appends missing closing delimiters for `` ` `` and ` ` ``` to ensure proper parsing.

2. **Extract and Convert Code Blocks**: Extracts Markdown code blocks, converts them to HTML `<pre><code>` format, and replaces them with placeholders to prevent formatting within code blocks.

3. **Markdown to HTML Conversion**: Applies various regex substitutions and custom logic to convert supported Markdown formatting to Telegram-compatible HTML tags.

4. **Reinsert Code Blocks**: Reinserts the previously extracted and converted code blocks back into the main text, replacing placeholders with the appropriate HTML content.

Simply call the `telegram_format(text: str) -> str` function with your Markdown-formatted text as input to receive the converted HTML output ready for use with the Telegram Bot API.

## Installation

You can install the package using pip:

```sh
pip install chatgpt-md-converter
```

## Example

````python
from chatgpt_md_converter import telegram_format

# Basic formatting
text = """
Here is some **bold**, __underline__, and `inline code`.
This is a ||spoiler text||.

```python
print('Hello, world!')
````

"""

# Blockquotes

blockquote_text = """

> Regular blockquote
> Multiple lines

\*\*>Expandable blockquote

> Hidden by default
> Multiple lines
> """

formatted_text = telegram_format(text)
formatted_blockquote = telegram_format(blockquote_text)

print(formatted_text)
print(formatted_blockquote)

```

## Requirements

- Python 3.x
- No external libraries required (uses built-in `re` module for regex operations)

## Contribution

Feel free to contribute to this project by submitting pull requests or opening issues for bugs, feature requests, or improvements.
```
