"""
statistics/github_rest.py

Low-level wrapper around GitHub REST API.
Responsible ONLY for making authenticated requests.
"""

import os
import requests


class GitHubREST:

    BASE_URL = "https://api.github.com"

    def __init__(self):

        token = os.getenv("ACCESS_TOKEN")

        if not token:
            raise RuntimeError(
                "ACCESS_TOKEN environment variable not found."
            )

        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        })

    # ----------------------------------------------------------

    def get(self, endpoint, params=None):
        """
        Generic GET request.
        """

        response = self.session.get(
            self.BASE_URL + endpoint,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    # ----------------------------------------------------------

    def get_user_commits(
        self,
        owner,
        repo,
        author,
        page=1,
        per_page=100
    ):
        """
        Returns commits authored by 'author'
        inside a repository.
        """

        return self.get(

            f"/repos/{owner}/{repo}/commits",

            {

                "author": author,

                "page": page,

                "per_page": per_page

            }

        )

    # ----------------------------------------------------------

    def get_commit(
        self,
        owner,
        repo,
        sha
    ):
        """
        Returns full information about
        a single commit.
        """

        return self.get(

            f"/repos/{owner}/{repo}/commits/{sha}"

        )


github_rest = GitHubREST()