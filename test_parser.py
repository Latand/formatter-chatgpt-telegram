from chatgpt_parser import split_by_tag, telegram_format
import pytest

def test_split_by_tag_bold():
    text = "This is **bold** text"
    assert split_by_tag(text, "**", "b") == "This is <b>bold</b> text"


def test_telegram_format_italic():
    text = "This is _italic_ text"
    output, format = telegram_format(text)
    assert output == "This is <i>italic</i> text"
    assert format == "HTML"


def test_telegram_format_italic_star():
    text = "This is *italic* text"
    output, format = telegram_format(text)
    assert output == "This is <i>italic</i> text"
    assert format == "HTML"


def test_triple_backticks_with_language():
    input_text = "```python\nprint('Hello, world!')\n```"
    expected_output = (
        "<pre><code class=\"language-python\">print('Hello, world!')\n</code></pre>"
    )
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed converting triple backticks with language to <pre><code> tags"


def test_bold_and_underline_conversion():
    input_text = "This is **bold** and this is __underline__."
    expected_output = "This is <b>bold</b> and this is <u>underline</u>."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed converting ** and __ to <b> and <u> tags"


def test_escaping_special_characters():
    input_text = "Avoid using < or > in your HTML."
    expected_output = "Avoid using &lt; or &gt; in your HTML."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed escaping < and > characters"


def test_nested_markdown_syntax():
    input_text = "This is **bold and _italic_** text."
    expected_output = "This is <b>bold and <i>italic</i></b> text."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed handling nested markdown syntax"


def test_combination_of_markdown_elements():
    input_text = """
# Heading
This is a test of **bold**, __underline__, and `inline code`.
- Item 1
* Item 2

```python
for i in range(3):
    print(i)
```

[Link](http://example.com)
"""
    expected_output = """<b>Heading</b>\nThis is a test of <b>bold</b>, <u>underline</u>, and <code>inline code</code>.\n• Item 1\n• Item 2\n\n<pre><code class="language-python">for i in range(3):\n    print(i)\n</code></pre>\n\n<a href="http://example.com">Link</a>\n"""
    output, format = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip() and format == "HTML"
    ), "Failed combining multiple markdown elements into HTML"


def test_nested_bold_within_italic():
    input_text = "This is *__bold within italic__* text."
    expected_output = "This is <i><u>bold within italic</u></i> text."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed converting nested bold within italic markdown to HTML"


def test_italic_within_bold():
    input_text = "This is **bold and _italic_ together**."
    expected_output = "This is <b>bold and <i>italic</i> together</b>."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed converting italic within bold markdown to HTML"


def test_inline_code_within_bold_text():
    input_text = "This is **bold and `inline code` together**."
    expected_output = "This is <b>bold and <code>inline code</code> together</b>."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed handling inline code within bold text"


def test_mixed_formatting_tags_with_lists_and_links():
    input_text = """
- This is a list item with **bold**, __underline__, and [a link](http://example.com)
- Another item with ***bold and italic*** text
"""
    expected_output = """
• This is a list item with <b>bold</b>, <u>underline</u>, and <a href="http://example.com">a link</a>
• Another item with <b><i>bold and italic</i></b> text
"""
    output, format = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed handling mixed formatting tags with lists and links"


def test_special_characters_within_code_blocks():
    input_text = "Here is a code block: ```<script>alert('Hello')</script>```"
    expected_output = (
        "Here is a code block: <pre><code><script>alert('Hello')</script></code></pre>"
    )
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed escaping special characters within code blocks"


def test_code_block_within_bold_text():
    input_text = "This is **bold with a `code block` inside**."
    expected_output = "This is <b>bold with a <code>code block</code> inside</b>."
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed handling code block within bold text"


def test_triple_backticks_with_nested_markdown():
    input_text = "```python\n**bold text** and __underline__ in code block```"
    # Expecting the markdown syntax to be ignored within the code block
    expected_output = '<pre><code class="language-python">**bold text** and __underline__ in code block</code></pre>'
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed handling markdown within triple backtick code blocks"


def test_unmatched_code_delimiters():
    input_text = "This has an `unmatched code delimiter."
    # Expecting original input as output due to the unmatched delimiter
    expected_output = "This has an <code>unmatched code delimiter.</code>"
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed handling unmatched code delimiters"


def test_preformatted_block_with_unusual_language_specification():
    input_text = "```weirdLang\nSome weirdLang code\n```"
    expected_output = (
        '<pre><code class="language-weirdLang">Some weirdLang code\n</code></pre>'
    )
    output, format = telegram_format(input_text)
    assert (
        output == expected_output and format == "HTML"
    ), "Failed handling preformatted block with unusual language specification"


def test_inline_code_within_lists():
    input_text = """
- List item with `code`
* Another `code` item
"""
    expected_output = """
• List item with <code>code</code>
• Another <code>code</code> item
"""
    output, format = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip() and format == "HTML"
    ), "Failed handling inline code within lists"

def test_vector_storage_links_trim():
    input_text = """
- List item with `code`
* Another `code` item【4:0†source】
"""
    expected_output = """
• List item with <code>code</code>
• Another <code>code</code> item
"""
    output, format = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip() and format == "HTML"
    ), "Failed trim storage links"
