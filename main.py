"""
main.py

Entry point for the GitHub Terminal Dashboard.
"""

import time
from dotenv import load_dotenv

load_dotenv()

from renderer import renderer
from github_api import github
from github_stats.statistics_manager import get_statistics


def banner():
    print("=" * 60)
    print(" GitHub Terminal Dashboard Generator")
    print("=" * 60)


def main():

    banner()

    start = time.perf_counter()

    print("[1/4] Fetching GitHub profile...")
    profile = github.get_profile()

    print("[2/4] Calculating GitHub statistics...")
    stats = get_statistics()

    print("[3/4] Rendering README...")
    renderer.render(profile, stats)

    elapsed = time.perf_counter() - start

    print("[4/4] Done!")

    print()
    print("=" * 60)
    print(f"Repositories : {profile['repositories']}")
    print(f"Followers    : {profile['followers']}")
    print(f"Stars        : {profile['stars']}")
    print(f"Commits      : {stats['commits']}")
    print(f"Lines Added  : {stats['additions']:,}")
    print(f"Lines Deleted: {stats['deletions']:,}")
    print(f"Net LOC      : {stats['additions'] - stats['deletions']:,}")
    print("=" * 60)
    print(f"Finished in {elapsed:.2f}s")


if __name__ == "__main__":
    main()