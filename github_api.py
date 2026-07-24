"""
github_api.py

Wrapper around GitHub GraphQL API.
"""

import os
import requests

from config import config


class GitHubAPI:
    GRAPHQL_URL = "https://api.github.com/graphql"

    def __init__(self):
        token = os.getenv("ACCESS_TOKEN")

        if not token:
            raise EnvironmentError(
                "ACCESS_TOKEN environment variable not found."
            )

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        self.username = config.github_username

    # --------------------------------------------------

    def _query(self, query: str, variables=None):
        """
        Execute a GraphQL query.
        """

        response = requests.post(
            self.GRAPHQL_URL,
            json={
                "query": query,
                "variables": variables or {},
            },
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise Exception(data["errors"])

        return data["data"]

    # --------------------------------------------------

    def get_profile(self):
        """
        Returns summarized profile information.
        """

        query = """
        query($login: String!) {
          user(login: $login) {

            name
            login

            followers {
              totalCount
            }

            following {
              totalCount
            }

            repoCount: repositories(
              ownerAffiliations: OWNER
            ) {
              totalCount
            }

            repositoriesContributedTo {
              totalCount
            }

            contributionsCollection {
              contributionCalendar {
                totalContributions
              }
            }

            repoList: repositories(
              first: 100,
              ownerAffiliations: OWNER
            ) {
              nodes {
                stargazerCount
              }
            }

          }
        }
        """

        data = self._query(
            query,
            {
                "login": self.username,
            },
        )

        user = data["user"]

        total_stars = sum(
            repo["stargazerCount"]
            for repo in user["repoList"]["nodes"]
        )

        return {
            "name": user["name"],
            "username": user["login"],
            "followers": user["followers"]["totalCount"],
            "following": user["following"]["totalCount"],
            "repositories": user["repoCount"]["totalCount"],
            "contributed_repositories": user["repositoriesContributedTo"]["totalCount"],
            "contributions": user["contributionsCollection"][
                "contributionCalendar"
            ]["totalContributions"],
            "stars": total_stars,
        }

    # --------------------------------------------------

    def get_repositories(self):
        """
        Returns repository metadata needed by the statistics module.
        """

        query = """
        query($login: String!) {

          user(login: $login) {

            repositories(
              first: 100,
              ownerAffiliations: OWNER,
              orderBy: {
                field: UPDATED_AT,
                direction: DESC
              }
            ) {

              nodes {

                name
                description
                url

                isFork
                isArchived
                isPrivate

                stargazerCount
                forkCount

                defaultBranchRef {
                  name
                }

                owner {
                  login
                }

                primaryLanguage {
                  name
                }

              }

            }

          }

        }
        """

        data = self._query(
            query,
            {
                "login": self.username,
            },
        )

        return data["user"]["repositories"]["nodes"]


github = GitHubAPI()