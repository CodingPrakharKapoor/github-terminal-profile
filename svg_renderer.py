"""
svg_renderer.py

SVG renderer for the GitHub Terminal Profile.
"""

from pathlib import Path
from xml.sax.saxutils import escape


class SVGRenderer:

    # ------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------

    def __init__(self):

        # Canvas

        self.width = 1200
        self.height = 700
        self.line_width = 42
        self.min_dots = 3

        # Layout

        self.padding = 30
        self.left_x = 30
        self.right_x = 420

        self.line_height = 22

        self.left_cursor = 50
        self.right_cursor = 50

        # Colors

        self.background = "#161b22"

        self.text = "#c9d1d9"

        self.key = "#ffa657"

        self.value = "#a5d6ff"

        self.green = "#3fb950"

        self.red = "#f85149"

        self.gray = "#8b949e"

        # SVG content

        self.elements = []

        self._create_background()
        # Typography

        self.font_family = "Consolas, 'Courier New', monospace"
        self.font_size = 18

        # Terminal columns (characters, not pixels)

        self.key_width = 20

    # ------------------------------------------------------------
    # Background
    # ------------------------------------------------------------

    def _create_background(self):

        self.elements.append(
            f'<rect width="{self.width}" height="{self.height}" fill="{self.background}" />'
        )

    # ------------------------------------------------------------
    # Resize canvas
    # ------------------------------------------------------------

    def set_size(self, width, height):

        self.width = width
        self.height = height

        self.elements[0] = (
            f'<rect width="{self.width}" '
            f'height="{self.height}" '
            f'fill="{self.background}" />'
        )

    # ------------------------------------------------------------
    # Generic text
    # ------------------------------------------------------------

    def text_at(
        self,
        x,
        y,
        text,
        color=None,
        size=18,
        weight="normal",
    ):

        color = color or self.text

        text = escape(str(text))

        self.elements.append(
            f'''
<text
    x="{x}"
    y="{y}"
    fill="{color}"
    font-family="Consolas, 'Courier New', monospace"
    font-size="{size}"
    font-weight="{weight}">
{text}
</text>
'''.strip()
        )

    # ------------------------------------------------------------
    # Left column
    # ------------------------------------------------------------

    def left(self, text, color=None, size=18):

        self.text_at(
            self.left_x,
            self.left_cursor,
            text,
            color=color,
            size=size,
        )

        self.left_cursor += self.line_height

    # ------------------------------------------------------------
    # Right column
    # ------------------------------------------------------------

    def right(self, text, color=None, size=18):

        self.text_at(
            self.right_x,
            self.right_cursor,
            text,
            color=color,
            size=size,
        )

        self.right_cursor += self.line_height

    # ------------------------------------------------------------
    # Blank line
    # ------------------------------------------------------------

    def blank_left(self):

        self.left_cursor += self.line_height

    def blank_right(self):

        self.right_cursor += self.line_height

    # ------------------------------------------------------------
    # ASCII renderer
    # ------------------------------------------------------------

    def add_ascii(self, ascii_art):

        if isinstance(ascii_art, str):
            lines = ascii_art.splitlines()
        else:
            lines = ascii_art

        for line in lines:
            self.left(line)

    # ------------------------------------------------------------
    # Title
    # ------------------------------------------------------------

    def title(self, title):

        self.right(
            title,
            color=self.value,
            size=24,
        )

    # ------------------------------------------------------------
    # Subtitle
    # ------------------------------------------------------------

    def subtitle(self, text):

        self.right(
            text,
            color=self.gray,
            size=16,
        )

    # ------------------------------------------------------------
    # Horizontal divider
    # ------------------------------------------------------------

    def divider(self):

        self.right(
            "—" * self.line_width,
            color=self.gray,
        )

    # ------------------------------------------------------------
    # Auto resize height
    # ------------------------------------------------------------

    def fit_height(self):

        lowest = max(
            self.left_cursor,
            self.right_cursor,
        )

        self.set_size(
            self.width,
            lowest + self.padding,
        )

    # ------------------------------------------------------------
    # Save
    # ------------------------------------------------------------

    def save(self, filename="terminal.svg"):

        self.fit_height()

        svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{self.width}"
height="{self.height}"
viewBox="0 0 {self.width} {self.height}">

{"".join(self.elements)}

</svg>
'''

        Path(filename).write_text(
            svg,
            encoding="utf-8",
        )

    # ------------------------------------------------------------
    # Key / Value Line
    # ------------------------------------------------------------

    def key_value(
        self,
        key,
        value,
        key_color=None,
        value_color=None,
    ):

        key_color = key_color or self.key
        value_color = value_color or self.value

        key = escape(str(key))
        value = escape(str(value))

        # dots = "." * max(2, self.key_width - len(str(key)))
        dots = "." * max(
            self.min_dots,
            self.line_width - len(key) - len(value)
        )

        self.elements.append(
            f"""
    <text
        x="{self.right_x}"
        y="{self.right_cursor}"
        font-family="{self.font_family}"
        font-size="{self.font_size}">

    <tspan fill="{key_color}">{key}</tspan><tspan fill="{self.gray}">{dots}</tspan><tspan fill="{value_color}">{value}</tspan>

    </text>
    """.strip()
        )

        self.right_cursor += self.line_height
    # ------------------------------------------------------------
    # Section Heading
    # ------------------------------------------------------------

    def section_heading(self, title):

        self.right(
            title,
            color=self.value,
            size=20,
        )

        self.divider()

    # ------------------------------------------------------------
    # Complete Section
    # ------------------------------------------------------------

    def section(self, title, rows):

        self.section_heading(title)

        for key, value in rows:
            self.key_value(key, value)

        self.blank_right()

    # ------------------------------------------------------------
    # Colored Statistics
    # ------------------------------------------------------------

    def statistic(self, key, value):

        color = self.value

        if isinstance(value, (int, float)):
            value = f"{value:,}"

        value = str(value)

        if value.startswith("+"):
            color = self.green

        elif value.startswith("-"):
            color = self.red

        self.key_value(
            key,
            value,
            value_color=color,
        )


renderer = SVGRenderer()