"""
renderer.py

Renders README.md from template.md
"""

from jinja2 import Environment, FileSystemLoader

from config import config
from utils import (
    calculate_age,
    list_to_string,
    load_ascii,
    write_file,
)


class Renderer:

    def __init__(self):

        self.env = Environment(
            loader=FileSystemLoader("."),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    # --------------------------------------------------

    def build_context(self, profile, statistics):
        """
        Creates the dictionary passed into Jinja2.
        """

        return {

            # Personal
            "name": config.name,
            "title": config.title,
            "subtitle": config.subtitle,
            "location": config.location,
            "email": config.email,
            "website": config.website,

            # GitHub
            "github": profile,

            # Statistics
            "statistics": statistics,

            # Age
            "age": calculate_age(config.birthday),

            # Skills
            "languages": list_to_string(config.languages),
            "frameworks": list_to_string(config.frameworks),
            "databases": list_to_string(config.databases),
            "tools": list_to_string(config.tools),

            # Projects
            "projects": config.current_projects,

            # Achievements
            "achievements": config.achievements,

            # Socials
            "socials": config.socials,

            # ASCII
            "ascii": load_ascii(config.theme["ascii_file"]),

            # UI
            "sections": config.sections,
        }

    # --------------------------------------------------

    def render(self, profile, statistics):

        template = self.env.get_template(
            config.theme["template"]
        )

        output = template.render(
            self.build_context(profile, statistics)
        )

        write_file(
            "README.md",
            output
        )

        print("README.md generated successfully.")


renderer = Renderer()