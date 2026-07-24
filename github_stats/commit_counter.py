from github_stats.github_rest import github_rest
from github_stats.cache import cache
from config import config
import requests


def process_repository(repository):
    """
    Updates commit statistics for a single repository.

    Parameters
    ----------
    repository : dict
        {
            "owner": "...",
            "name": "...",
            ...
        }

    Returns
    -------
    dict
        {
            "repository": "...",
            "commits": int,
            "additions": int,
            "deletions": int
        }
    """

    owner = repository["owner"]
    repo = repository["name"]

    key = f"{owner}/{repo}"

    cached = cache.load(key)

    if cached and cached.get("empty"):
        return {
            "repository": repo,
            "commits": 0,
            "additions": 0,
            "deletions": 0
        }
    
    if cached is None:
        cached = {
            "statistics": {
                "commits": 0,
                "additions": 0,
                "deletions": 0
            },
            "last_processed_sha": None
        }

    stats = cached["statistics"]

    newest_sha = None
    page = 1

    while True:

        try:
            commits = github_rest.get_user_commits(
                owner,
                repo,
                config.github_username,
                page=page
            )

        except requests.exceptions.HTTPError as e:

            if e.response.status_code == 409:

                print(f"Skipping empty repository: {owner}/{repo}")

                cache.save(
                    key,
                    {
                        "statistics": {
                            "commits": 0,
                            "additions": 0,
                            "deletions": 0
                        },
                        "last_processed_sha": None,
                        "empty": True
                    }
                )

                return {
                    "repository": repo,
                    "commits": 0,
                    "additions": 0,
                    "deletions": 0
                }

            raise

        if not commits:
            break

        stop = False

        for commit in commits:

            sha = commit["sha"]

            # First commit returned is always the newest one.
            if newest_sha is None:
                newest_sha = sha

            # Already processed
            if sha == cached["last_processed_sha"]:
                stop = True
                break

            details = github_rest.get_commit(
                owner,
                repo,
                sha
            )

            commit_stats = details.get("stats", {})

            stats["commits"] += 1
            stats["additions"] += commit_stats.get("additions", 0)
            stats["deletions"] += commit_stats.get("deletions", 0)

        if stop:
            break

        page += 1

    if newest_sha is not None:
        cached["last_processed_sha"] = newest_sha

    cache.save(key, cached)

    return {
        "repository": repo,
        "commits": stats["commits"],
        "additions": stats["additions"],
        "deletions": stats["deletions"]
    }