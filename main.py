from flask import Flask, jsonify
from github import Github, GithubException
from github import Auth
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_KEY = os.getenv('AUTH_KEY')

app = Flask(__name__)

@app.route('/github/user/commits/total')
def get_total_own_commits():

    auth = Auth.Token(AUTH_KEY)
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
        return jsonify({"error": str(e), "message": "Error fetching data from GitHub"}), 500

    return jsonify({"total_commits": total_own_commits})
if __name__ == '__main__':
    app.run(debug=True)
