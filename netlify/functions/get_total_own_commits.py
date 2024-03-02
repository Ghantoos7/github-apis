import os
import json
from github import Github, GithubException
from github.Auth import Token

def handler(event, context):
    AUTH_KEY = os.getenv('AUTH_KEY')
    auth = Token(AUTH_KEY)
    g = Github(auth=auth)

    total_own_commits = 0

    try:
        user = g.get_user()
        for repo in user.get_repos():
            try:
                commits = repo.get_commits(author=user.login)
                total_own_commits += commits.totalCount
            except GithubException as e:
                if e.status == 409:
                    continue
                else:
                    raise
    except GithubException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e), "message": "Error fetching data from GitHub"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "schemaVersion": 1,
            "label": "Total Commits",
            "message": str(total_own_commits),
            "color": "red"
        })
    }
