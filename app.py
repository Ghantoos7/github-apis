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


def fetch_repo_commits(repo, user_login):
    """Fetch commit count for a given repository and user."""
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
        repos = list(user.get_repos())
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_repo_commits, repo, user.login) for repo in repos]
            for future in as_completed(futures):
                total_own_commits += future.result()
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


def fetch_dir_contents(repo, dir_path):
    """Function to fetch contents of a given directory in a repository."""
    dir_contents = repo.get_contents(dir_path)
    easy_count = 0
    for dir_content in dir_contents:
        if dir_content.name == "README.md":
            if "Difficulty: Easy" in dir_content.decoded_content.decode("utf-8"):
                easy_count += 1
    return easy_count



@app.route('/github/user/repos/<repo_name>/easy/total')
@cache.cached(timeout=43200, key_prefix='easy_problems')
def get_easy_problems_count(repo_name):
    g = Github(login_or_token=AUTH_KEY)
    easy_count = 0
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        contents = repo.get_contents("")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_dir_contents, repo, content.path) for content in contents if content.type == "dir"]
            for future in as_completed(futures):
                easy_count += future.result()
    except GithubException as e:
        return jsonify({"error": str(e), "message": "Error fetching repository information"}), 500
    
    return jsonify({"schemaVersion": 1, "label": "Easy Problems", "message": str(easy_count), "color": "green"})

app.run(debug=True)
