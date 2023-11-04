import requests
import re
from urllib.parse import urlparse
from termcolor import colored

# Retrieve the personal access token from an environment variable
personal_access_token = "TOKENHERE"

# Replace 'username' with the actual GitHub username you're interested in
username = ""

if not username:
    username = input("What is the username of the GitHub to check?: ")

# Exit if the token is not set
if not personal_access_token:
    print("GitHub personal access token not found. Please set the GITHUB_TOKEN environment variable.")
    exit()

# Headers to be used for authorization and accepting JSON responses
headers = {
    'Authorization': f'token {personal_access_token}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_all_pages(url):
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            yield from response.json()
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            break

def get_commit_emails(username, repo_name):
    commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    commit_emails = []

    for commit in get_all_pages(commits_url):
        commit_url = f"https://github.com/{username}/{repo_name}/commit/{commit['sha']}.patch"
        patch_response = requests.get(commit_url, headers=headers)

        if patch_response.status_code == 200:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, patch_response.text)
            commit_emails.extend([(email, commit_url) for email in emails])
        else:
            print(f"Failed to retrieve patch for URL {commit_url}. Status code: {patch_response.status_code}")

    return commit_emails

def print_emails_nicely(emails_with_urls):
    emails_set = set()  # Use a set to automatically deduplicate emails
    for email, url in emails_with_urls:
        emails_set.add(email)  # Add to set for deduplication
        email_colored = colored(email, 'blue')
        url_colored = colored(url, 'green')
        print(f"Email: {email_colored} found at URL: {url_colored}")

    # Print separator and deduplicated emails
    print("\n" + "-" * 40 + "\nAll unique emails found:\n" + "-" * 40)
    for email in emails_set:
        print(colored(email, 'yellow'))

if __name__ == "__main__":
    repos_url = f"https://api.github.com/users/{username}/repos"
    all_emails_with_urls = []

    for repo in get_all_pages(repos_url):
        if not repo['fork']:
            print(f"Processing Repository: {repo['name']}")
            commit_emails = get_commit_emails(username, repo['name'])
            all_emails_with_urls.extend(commit_emails)

    # Once processing is done, print the emails and URLs nicely
    print_emails_nicely(all_emails_with_urls)
