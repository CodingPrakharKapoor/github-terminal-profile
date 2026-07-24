"""
github_stats/repository_fetcher.py

Responsible for fetching repositories that should be
included in statistics.
"""

from github_api import github


class RepositoryFetcher:

    def get_repositories(self):

        repositories = github.get_repositories()

        result = []

        for repo in repositories:

            result.append(
                {
                    "owner": repo["owner"]["login"],
                    "name": repo["name"],
                    "default_branch":
                        repo["defaultBranchRef"]["name"]
                        if repo["defaultBranchRef"]
                        else None,
                    "is_fork": repo["isFork"],
                    "is_archived": repo["isArchived"],
                    "is_private": repo["isPrivate"],
                }
            )

        return result


repository_fetcher = RepositoryFetcher()