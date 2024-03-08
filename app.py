from flask import Flask, jsonify
from flask_caching import Cache
from github import Github, GithubException
import os

AUTH_KEY = os.getenv('AUTH_KEY')

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 43200
cache = Cache(app)

@app.route('/github/user/commits/total')
@cache.cached(timeout=43200, key_prefix='total_own_commits')
def get_total_own_commits():
    g = Github(login_or_token=AUTH_KEY)
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
        return jsonify({"error": str(e), "message": "Error fetching data from GitHub"}), 500
    return jsonify({ "schemaVersion": 1, "label": "Total Commits", "message": str(total_own_commits), "color": "red" })

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

# 'Difficulty: Easy'
# every directory has a README.md file inside the md file i want to check for the occurence of 'Difficulty: Easy'
@app.route('/github/user/repos/<repo_name>/easy/total')
def get_easy_problems_count(repo_name):
    g = Github(login_or_token=AUTH_KEY)
    easy_count = 0
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        contents = repo.get_contents("")
        for content in contents:
            if content.type == "dir":
                dir_contents = repo.get_contents(content.path)
                for dir_content in dir_contents:
                    if dir_content.name == "README.md":
                        if "Difficulty: Easy" in dir_content.decoded_content.decode("utf-8"):
                            easy_count += 1
    except GithubException as e:
        return jsonify({"error": str(e), "message": "Error fetching repository information"}), 500
    
    return jsonify({"schemaVersion": 1, "label": "Easy Problems", "message": str(easy_count), "color": "green"})

app.run(debug=True)
