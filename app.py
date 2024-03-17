from flask import Flask, jsonify
from flask_caching import Cache
from github import Github, GithubException
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

AUTH_KEY = os.getenv('AUTH_KEY')

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 43200
cache = Cache(app)

def fetch_commit_count(repo, user_login):
    try:
        commits = repo.get_commits(author=user_login)
        return commits.totalCount
    except GithubException as e:
        if e.status == 409:  
            return 0
        else:
            raise


@app.route('/github/user/commits/total')
def get_total_own_commits():
    g = Github(login_or_token=AUTH_KEY)
    total_own_commits = 0
    try:
        user = g.get_user()
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_repo = {executor.submit(fetch_commit_count, repo, user.login): repo for repo in user.get_repos()}
            for future in as_completed(future_to_repo):
                try:
                    total_own_commits += future.result()
                except GithubException as e:
                    if e.status != 409:
                        return jsonify({"error": str(e), "message": "Error fetching commit count"}), 500
    except GithubException as e:
        return jsonify({"error": str(e), "message": "Error fetching data from GitHub"}), 500
    return jsonify({"schemaVersion": 1, "label": "Total Commits", "message": str(total_own_commits), "color": "red"})

@app.route('/github/user/repos/<repo_name>/folders')
def get_repo_folder_count(repo_name):
    g = Github(login_or_token=AUTH_KEY)
    folder_count = 0
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        contents = repo.get_contents("")
        for content in contents:
            if content.type == "dir":
                folder_count += 1
    except GithubException as e:
        return jsonify({"error": str(e), "message": "Error fetching repository information"}), 500
    return jsonify({"schemaVersion": 1, "label": "Total Problems Solved", "message": str(folder_count), "color": "blue"})

if __name__ == '__main__':
    app.run(debug=True)
