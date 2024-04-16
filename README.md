# GitHub Statistics API

This Flask application provides a simple API to fetch various statistics from a GitHub user's profile, such as total commits, repository folder counts, and counts of easy, medium, and hard leetcode problems that i solved based on README badges.  uses the GitHub API for data retrieval and leverages parallel processing and caching to optimize performance.

## Features

- **Total Own Commits**: Fetch the total number of commits made by a user across all their repositories.
- **Total Problems Solved**: Count the number of leetcode problems solved in.
- **Easy Problems Count**: Fetch the count of problems easy leetcode problems solved.
- **Medium Problems Count**:Fetch the count of problems meduim leetcode problems solved.
- **Hard Problems Count**: Fetch the count of problems hard leetcode problems solved.


## Parallel Processing

This application utilizes a `ThreadPoolExecutor` to manage parallel tasks efficiently. By processing multiple repositories or content checks concurrently, the API significantly improves data retrieval

## Setup

### Prerequisite

- Python 3.x
- Flask
- Flask-Caching
- PyGitHub
- BeautifulSoup4

### Installation

1. Clone the repo
```bash
git clone https://github.com/Ghantoos7/github-apis.git
cd github-apis
```


2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

- Obtain a GitHub Personal Access Token from https://github.com/settings/tokens and set it as AUTH_KEY in your environment.

4. Run the application:
```bash
python app.py
```

## Endpoints 

- **GET /github/user/commits/total**: Fetch the total number of commits made by the authenticated user.
- **GET /github/user/repos/<repo_name>/folders**: Retrieve the total number of folders in a specific repository.
- **GET /github/user/repos/<repo_name>/easy_problems_count:** Get the count of problems marked as 'Easy' in a repository.
- **GET /github/user/repos/<repo_name>/medium_problems_count**: Get the count of problems marked as 'Medium' in a repository.
- **GET /github/user/repos/<repo_name>/hard_problems_count**: Get the count of problems marked as 'Hard' in a repository.

Make sure to replace the repo_name with the name of the repo that contains your leetcode problems.

## Usage

Deploy the app on either [Heroku](https://heroku.com) or on [Vercel](https://vercel.com), and use the endpoint component on [Shields.io](https://shields.io/) to show it as a badge.

## TO DO

1. Add more APIs.
2. Optimize performance even more.


## Contribuation

Feel free to add new apis or to suggest new ideas to me on via [linkedin](https://www.linkedin.com/in/georgio-ghnatios-33a295222/) 

## License
This project is licensed under the MIT License.

