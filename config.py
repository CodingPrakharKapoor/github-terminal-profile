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

        with open(config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)

    # -------------------------
    # Internal helper
    # -------------------------

    def _get(self, *keys, default=None):
        """
        Safely retrieve nested values.

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

    # -------------------------
    # Personal
    # -------------------------

    @property
    def name(self):
        return self._get("personal", "name")

    @property
    def title(self):
        return self._get("personal", "title")

    @property
    def subtitle(self):
        return self._get("personal", "subtitle")

    @property
    def github_username(self):
        return self._get("personal", "github_username")

    @property
    def birthday(self):
        return self._get("personal", "birthday")

    @property
    def location(self):
        return self._get("personal", "location")

    @property
    def email(self):
        return self._get("personal", "email")

    @property
    def website(self):
        return self._get("personal", "website")

    # -------------------------
    # Socials
    # -------------------------

    @property
    def socials(self):
        return self._get("socials", default={})

    # -------------------------
    # System
    # -------------------------

    @property
    def system(self):
        return self._get("system", default={})

    # -------------------------
    # Skills
    # -------------------------

    @property
    def languages(self):
        return self._get("languages", default=[])

    @property
    def frameworks(self):
        return self._get("frameworks", default=[])

    @property
    def databases(self):
        return self._get("databases", default=[])

    @property
    def tools(self):
        return self._get("tools", default=[])

    # -------------------------
    # Projects / Achievements
    # -------------------------

    @property
    def current_projects(self):
        return self._get("currently_working_on", default=[])

    @property
    def achievements(self):
        return self._get("achievements", default=[])

    # -------------------------
    # UI Sections
    # -------------------------

    @property
    def sections(self):
        return self._get("sections", default={})

    # -------------------------
    # Theme
    # -------------------------

    @property
    def theme(self):
        return self._get("theme", default={})


# Singleton instance used throughout the project
config = Config()