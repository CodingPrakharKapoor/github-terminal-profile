"""
loc_counter.py

Counts:
    - Lines Added
    - Lines Deleted
    - Total Commits

Only counts commits authored by the configured GitHub user.
"""

import requests
import os

from config import config


class LOCCounter:

    GRAPHQL_URL = "https://api.github.com/graphql"

    def __init__(self):

        token = os.getenv("ACCESS_TOKEN")

        if not token:
            raise RuntimeError("ACCESS_TOKEN not found.")

        self.headers = {
            "Authorization": f"Bearer {token}"
        }

        self.username = config.github_username

        self.owner_id = self.get_owner_id()

    # --------------------------------------------------

    def query(self, query, variables):

        response = requests.post(
            self.GRAPHQL_URL,
            json={
                "query": query,
                "variables": variables
            },
            headers=self.headers
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise Exception(data["errors"])

        return data["data"]

    # --------------------------------------------------

    def get_owner_id(self):

        query = """
        query($login:String!)
        {
            user(login:$login){
                id
            }
        }
        """

        return self.query(
            query,
            {
                "login": self.username
            }
        )["user"]["id"]

    # --------------------------------------------------

    def repositories(self):

        cursor = None

        while True:

            query = """
            query($login:String!,$cursor:String)
            {
              user(login:$login){

                repositories(
                    first:100,
                    after:$cursor,
                    ownerAffiliations:OWNER
                ){

                    nodes{
                        name
                    }

                    pageInfo{
                        hasNextPage
                        endCursor
                    }

                }

              }
            }
            """

            data = self.query(
                query,
                {
                    "login": self.username,
                    "cursor": cursor
                }
            )

            repos = data["user"]["repositories"]

            for repo in repos["nodes"]:
                yield repo["name"]

            if not repos["pageInfo"]["hasNextPage"]:
                break

            cursor = repos["pageInfo"]["endCursor"]

    # --------------------------------------------------

    def repository_loc(self, repo):

        additions = 0
        deletions = 0
        commits = 0

        cursor = None

        while True:

            query = """
            query($owner:String!,
                  $repo:String!,
                  $cursor:String){

              repository(
                owner:$owner,
                name:$repo
              ){

                defaultBranchRef{

                  target{

                    ... on Commit{

                      history(
                        first:100,
                        after:$cursor
                      ){

                        nodes{

                          additions

                          deletions

                          author{

                            user{

                              id

                            }

                          }

                        }

                        pageInfo{

                          hasNextPage

                          endCursor

                        }

                      }

                    }

                  }

                }

              }

            }
            """

            data = self.query(
                query,
                {
                    "owner": self.username,
                    "repo": repo,
                    "cursor": cursor
                }
            )

            branch = data["repository"]["defaultBranchRef"]

            if branch is None:
                break

            history = branch["target"]["history"]

            for commit in history["nodes"]:

                author = commit["author"]

                if author and author["user"]:

                    if author["user"]["id"] == self.owner_id:

                        additions += commit["additions"]

                        deletions += commit["deletions"]

                        commits += 1

            if not history["pageInfo"]["hasNextPage"]:
                break

            cursor = history["pageInfo"]["endCursor"]

        return additions, deletions, commits

    # --------------------------------------------------

    def calculate(self):

        total_add = 0

        total_del = 0

        total_commits = 0

        for repo in self.repositories():

            print(f"Scanning {repo}...")

            add, delete, commits = self.repository_loc(repo)

            total_add += add

            total_del += delete

            total_commits += commits

        return {

            "additions": total_add,

            "deletions": total_del,

            "total": total_add - total_del,

            "commits": total_commits

        }


loc = LOCCounter()