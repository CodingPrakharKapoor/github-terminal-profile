"""
renderer.py

Renders README.md from template.md
"""

from jinja2 import Environment, FileSystemLoader

from config import config
from utils import (
    calculate_uptime,
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

        user = {
            "name": config.name,
            "title": config.title,
            "subtitle": config.subtitle,
            "location": config.location,
            "email": config.email,
            "website": config.website,
            "uptime": calculate_uptime(config.birthday),
        }

        skills = {
            "languages": list_to_string(config.languages),
            "frameworks": list_to_string(config.frameworks),
            "databases": list_to_string(config.databases),
            "tools": list_to_string(config.tools),
        }

        return {

            # New grouped dictionaries
            "user": user,
            "github": profile,
            "statistics": statistics,
            "skills": skills,

            # Projects
            "projects": config.current_projects,

            # Achievements
            "achievements": config.achievements,

            # Socials
            "socials": config.socials,

            # ASCII Art
            "ascii": load_ascii(config.theme["ascii_file"]),

            # UI
            "sections": config.sections,

            # ------------------------------------------------------------------
            # Backward compatibility
            # These allow the existing template.md to work unchanged.
            # They can be removed later after template.md is updated.
            # ------------------------------------------------------------------

            "name": user["name"],
            "title": user["title"],
            "subtitle": user["subtitle"],
            "location": user["location"],
            "email": user["email"],
            "website": user["website"],

            # Replaces age with uptime while keeping the template unchanged.
            "age": user["uptime"],

            "languages": skills["languages"],
            "frameworks": skills["frameworks"],
            "databases": skills["databases"],
            "tools": skills["tools"],
        }

    # --------------------------------------------------

    def render(self, profile, statistics):

        template = self.env.get_template(
            config.theme["template"]
        )

        context = self.build_context(profile, statistics)

        output = template.render(context)

        write_file(
            "README.md",
            output
        )

        print("README.md generated successfully.")


renderer = Renderer()