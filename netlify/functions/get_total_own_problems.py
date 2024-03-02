import os
import json
from github import Github, GithubException
from github.Auth import Token

def handler(event, context):
    AUTH_KEY = os.getenv('AUTH_KEY')
    auth = Token(AUTH_KEY)
    g = Github(auth=auth)

    total_own_problems = 0

    try:
        user = g.get_user()
        repo = user.get_repo("LeetCode-Problems")
        contents = repo.get_contents("")
        for content_file in contents:
            if content_file.type == "dir":
                total_own_problems += 1
    except GithubException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "message": "Error fetching data from GitHub",
                "Auth key is set": AUTH_KEY is not None
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "schemaVersion": 1,
            "label": "Total Problems Solved",
            "message": str(total_own_problems),
            "color": "blue"
        })
    }