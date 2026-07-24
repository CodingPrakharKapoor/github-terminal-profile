from github_stats.repository_fetcher import repository_fetcher
from github_stats.commit_counter import process_repository


def get_statistics():
    """
    Processes every repository and returns overall GitHub statistics.

    Returns
    -------
    dict
        {
            "commits": int,
            "additions": int,
            "deletions": int,
            "repositories": [
                ...
            ]
        }
    """

    repositories = repository_fetcher.get_repositories()

    print(repositories[0])

    totals = {
        "commits": 0,
        "additions": 0,
        "deletions": 0,
        "repositories": []
    }

    for repository in repositories:

        stats = process_repository(repository)

        totals["commits"] += stats["commits"]
        totals["additions"] += stats["additions"]
        totals["deletions"] += stats["deletions"]

        totals["repositories"].append(stats)

    return totals