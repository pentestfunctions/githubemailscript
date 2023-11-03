import requests
import re

# Create token below (Give it any name/expiration time and just give ie access to read Public Repositories)
# Uses tokens otherwise API rate limits: https://github.com/settings/tokens/new
personal_access_token = 'TEST_CODE'

# Replace 'username' with the actual GitHub username you're interested in
username = "pentestfunctions"
repos_url = f"https://api.github.com/users/{username}/repos"

# Headers to be used for authorization
headers = {
    'Authorization': f'token {personal_access_token}'
}

def get_commit_urls(username, repo_name):
    commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    commits_response = requests.get(commits_url, headers=headers)

    if commits_response.status_code == 200:
        commits = commits_response.json()
        commit_urls = [f"https://github.com/{username}/{repo_name}/commit/{commit['sha']}.patch" for commit in commits]
        return commit_urls
    else:
        print(f"Failed to retrieve commits for repository {repo_name}. Status code: {commits_response.status_code}")
        return []

def check_email_in_patch(patch_url):
    patch_response = requests.get(patch_url, headers=headers)  # Include headers here

    if patch_response.status_code == 200:
        # Regex pattern for matching email addresses
        email_pattern = (r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|'
                         r'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\'
                         r'[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.'
                         r')+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?'
                         r'[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|'
                         r'[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|'
                         r'\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')
        emails = re.findall(email_pattern, patch_response.text)
        return emails
    else:
        print(f"Failed to retrieve patch for URL {patch_url}. Status code: {patch_response.status_code}")
        return []

# Perform the GET request for the repositories
repos_response = requests.get(repos_url, headers=headers)

# Check if the request was successful
if repos_response.status_code == 200:
    # Parse the response JSON and iterate through the repositories
    repositories = repos_response.json()
    for repo in repositories:
        # Check if the repo is a fork
        if not repo['fork']:
            print(f"Repository: {repo['name']}")
            # Get the commit patch URLs for the repository
            commit_patch_urls = get_commit_urls(username, repo['name'])
            for patch_url in commit_patch_urls:
                emails = check_email_in_patch(patch_url)
                if emails:
                    print(f"Commit patch URL: {patch_url} contains emails: {emails}")
                else:
                    print(f"Commit patch URL: {patch_url} contains no emails.")
else:
    print(f"Failed to retrieve repositories for user {username}. Status code: {repos_response.status_code}")
