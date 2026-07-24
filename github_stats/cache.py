"""
github_stats/cache.py

Simple JSON-based cache manager.

This module is intentionally generic and has no knowledge
of GitHub repositories or statistics.
"""

from pathlib import Path
import json


class Cache:

    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------

    def _path(self, key: str) -> Path:
        """
        Convert a cache key into a JSON file path.

        Example:
            CodingPrakharKapoor/github-terminal-profile
        becomes
            cache/CodingPrakharKapoor/github-terminal-profile.json
        """

        key = key.replace("\\", "/")

        return self.cache_dir.joinpath(*key.split("/")).with_suffix(".json")

    # --------------------------------------------------

    def exists(self, key: str) -> bool:
        return self._path(key).exists()

    # --------------------------------------------------

    def load(self, key: str):
        """
        Returns cached object or None.
        """

        path = self._path(key)

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    # --------------------------------------------------

    def save(self, key: str, data):
        """
        Saves object as JSON.
        """

        path = self._path(key)

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------

    def delete(self, key: str):
        """
        Deletes cache entry if present.
        """

        path = self._path(key)

        if path.exists():
            path.unlink()

    # --------------------------------------------------

    def clear(self):
        """
        Removes every cached JSON file.
        """

        for file in self.cache_dir.rglob("*.json"):
            file.unlink()


cache = Cache()