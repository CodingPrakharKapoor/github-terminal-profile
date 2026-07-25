"""
main.py

Entry point for the GitHub Terminal Profile Generator.
"""

import time

from dotenv import load_dotenv

load_dotenv()

from config import config
from github_api import github
from github_stats.statistics_manager import get_statistics
from renderer import renderer


# ---------------------------------------------------------
# Banner
# ---------------------------------------------------------

def banner():

    print("=" * 60)
    print(" GitHub Terminal Profile Generator")
    print("=" * 60)


# ---------------------------------------------------------
# Build Data
# ---------------------------------------------------------

def build_profile_data():

    print("[1/4] Fetching GitHub profile...")
    github_profile = github.get_profile()

    print("[2/4] Calculating GitHub statistics...")
    github_statistics = get_statistics()

    return {
        "config": config,
        "github": github_profile,
        "statistics": github_statistics,
    }


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    banner()

    start = time.perf_counter()

    profile_data = build_profile_data()

    print("[3/4] Rendering output...")

    renderer.render(
        profile_data["github"],
        profile_data["statistics"],
    )

    elapsed = time.perf_counter() - start

    github_profile = profile_data["github"]
    github_statistics = profile_data["statistics"]

    print("[4/4] Done!")

    print()
    print("=" * 60)
    print(f"Repositories : {github_profile['repositories']}")
    print(f"Followers    : {github_profile['followers']}")
    print(f"Stars        : {github_profile['stars']}")
    print(f"Commits      : {github_statistics['commits']}")
    print(f"Lines Added  : {github_statistics['additions']:,}")
    print(f"Lines Deleted: {github_statistics['deletions']:,}")
    print(f"Net LOC      : {github_statistics['additions'] - github_statistics['deletions']:,}")
    print("=" * 60)
    print(f"Finished in {elapsed:.2f}s")


if __name__ == "__main__":
    main()