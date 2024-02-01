from flask import Flask, jsonify
from github import Github
from github import Auth
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

@app.route('/get_total_own_commits')
def get_total_own_commits():

    auth = Auth.Token(AUTH_KEY)
    g = Github(auth=auth)

    total_own_commits = 0

    user = g.get_user()

    for repo in user.get_repos():

        commits = repo.get_commits(author=user.login)
        total_own_commits += commits.totalCount

    return jsonify({"total_commits": total_own_commits})

if __name__ == '__main__':
    app.run(debug=True)
