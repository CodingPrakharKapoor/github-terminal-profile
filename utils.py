"""
utils.py

General helper functions used throughout the project.
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------
# UPTIME
# ---------------------------------------------------------

def calculate_uptime(birthday: str) -> str:
    """
    Calculates the time elapsed since the given birthday.

    Birthday format:
        YYYY-MM-DD

    Returns:
        22 years, 3 months, 14 days
    """

    birth = datetime.strptime(birthday, "%Y-%m-%d")
    now = datetime.now()

    diff = relativedelta(now, birth)

    return (
        f"{diff.years} year{'s' if diff.years != 1 else ''}, "
        f"{diff.months} month{'s' if diff.months != 1 else ''}, "
        f"{diff.days} day{'s' if diff.days != 1 else ''}"
    )


# ---------------------------------------------------------
# AGE (Backward Compatibility)
# ---------------------------------------------------------

def calculate_age(birthday: str) -> str:
    """
    Alias kept for backward compatibility.

    Existing code still calling calculate_age()
    will continue to work.
    """

    return calculate_uptime(birthday)


# ---------------------------------------------------------
# NUMBER FORMAT
# ---------------------------------------------------------

def format_number(number: int) -> str:
    """
    1234567

    ↓

    1,234,567
    """

    return f"{number:,}"


# ---------------------------------------------------------
# LIST FORMAT
# ---------------------------------------------------------

def list_to_string(items) -> str:
    """
    ["Java", "Python", "C++"]

    ↓

    Java, Python, C++
    """

    if not items:
        return ""

    return ", ".join(str(item) for item in items)


# ---------------------------------------------------------
# TERMINAL ALIGNMENT
# ---------------------------------------------------------

def terminal_line(title: str, value, width: int = 28) -> str:
    """
    Example

    Repositories.............53
    Followers...............210
    """

    dots = "." * max(2, width - len(title))

    return f"{title}{dots}{value}"


# ---------------------------------------------------------
# BOOLEAN
# ---------------------------------------------------------

def enabled(sections: dict, key: str) -> bool:
    """
    Returns whether a section is enabled.

    Missing key -> False
    """

    return sections.get(key, False)


# ---------------------------------------------------------
# READ FILE
# ---------------------------------------------------------

def read_file(filename: str) -> str:
    """
    Reads a UTF-8 text file.
    """

    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------
# WRITE FILE
# ---------------------------------------------------------

def write_file(filename: str, data: str):
    """
    Writes UTF-8 text.
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


# ---------------------------------------------------------
# ASCII ART
# ---------------------------------------------------------

def load_ascii(filename: str) -> str:
    """
    Loads ASCII art from a text file.
    """

    return read_file(filename)


# ---------------------------------------------------------
# MARKDOWN ESCAPE
# ---------------------------------------------------------

def escape_markdown(text: str) -> str:
    """
    Escapes characters that could interfere with Markdown.
    """

    if text is None:
        return ""

    text = str(text)

    replacements = {
        "|": "\\|",
        "*": "\\*",
        "_": "\\_",
        "`": "\\`",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text