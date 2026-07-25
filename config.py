"""
config.py

Loads and validates the application's configuration.
"""

from dotenv import load_dotenv

load_dotenv()

import json
from pathlib import Path


CONFIG_FILE = Path("config.json")


class Config:

    def __init__(self, config_path: Path = CONFIG_FILE):

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file '{config_path}' was not found."
            )

        with open(config_path, "r", encoding="utf-8") as file:
            self._config = json.load(file)

    # -------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------

    def _get(self, *keys, default=None):
        """
        Safely retrieves nested configuration values.

        Example:
            config._get("personal", "name")
        """

        value = self._config

        for key in keys:

            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value

    def section(self, name: str):
        """
        Returns an entire top-level section.

        Example:

            config.section("personal")
            config.section("socials")
        """

        return self._get(name, default={})

    # -------------------------------------------------
    # Generic Access
    # -------------------------------------------------

    def get(self, *keys, default=None):
        """
        Public generic getter.

        Examples

            config.get("personal", "name")

            config.get("system", "terminal")

            config.get("theme", "ascii_file")
        """

        return self._get(*keys, default=default)

    # -------------------------------------------------
    # Personal
    # -------------------------------------------------

    @property
    def personal(self):
        return self.section("personal")

    @property
    def name(self):
        return self.get("personal", "name")

    @property
    def title(self):
        return self.get("personal", "title")

    @property
    def subtitle(self):
        return self.get("personal", "subtitle")

    @property
    def github_username(self):
        return self.get("personal", "github_username")

    @property
    def birthday(self):
        return self.get("personal", "birthday")

    @property
    def location(self):
        return self.get("personal", "location")

    @property
    def email(self):
        return self.get("personal", "email")

    @property
    def website(self):
        return self.get("personal", "website")

    # -------------------------------------------------
    # Skills
    # -------------------------------------------------

    @property
    def languages(self):
        return self.get("languages", default=[])

    @property
    def frameworks(self):
        return self.get("frameworks", default=[])

    @property
    def databases(self):
        return self.get("databases", default=[])

    @property
    def tools(self):
        return self.get("tools", default=[])

    # -------------------------------------------------
    # Projects
    # -------------------------------------------------

    @property
    def current_projects(self):
        return self.get("currently_working_on", default=[])

    @property
    def achievements(self):
        return self.get("achievements", default=[])

    # -------------------------------------------------
    # Socials
    # -------------------------------------------------

    @property
    def socials(self):
        return self.get("socials", default={})

    # -------------------------------------------------
    # System
    # -------------------------------------------------

    @property
    def system(self):
        return self.get("system", default={})

    # -------------------------------------------------
    # Theme
    # -------------------------------------------------

    @property
    def theme(self):
        return self.get("theme", default={})

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    @property
    def sections(self):
        return self.get("sections", default={})

    # -------------------------------------------------
    # Entire Configuration
    # -------------------------------------------------

    @property
    def raw(self):
        """
        Returns the entire configuration dictionary.
        """

        return self._config


config = Config()