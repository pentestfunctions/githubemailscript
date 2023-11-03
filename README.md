# GitHub Email Scraper

This Python script is designed to scrape email addresses from commit patches of a given user's GitHub repositories that are not forks. It uses GitHub's REST API to retrieve repository and commit information.

## Features

- Fetch all repositories for a specified GitHub user
- Access detailed commit data for each repository
- Extract email addresses from commit patches
- Filter out forked repositories to only scan original content

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x
- You have a GitHub account and have generated a personal access token with the `public_repo` scope. Tokens can be created at: https://github.com/settings/tokens/new

## Setup and Installation

1. Clone the repository or download the script file to your local machine.
2. Install the required Python packages by running `pip install requests`.
3. Edit the script to include your personal access token where `personal_access_token = 'TEST_CODE'` is mentioned.

## Usage

After setting up the script with your personal access token, follow these steps:

1. Replace `'pentestfunctions'` with the username of the GitHub user you're interested in scraping emails from.

    ```python
    username = "target_username"
    ```

2. Run the script in your terminal:

    ```sh
    python github_email_scraper.py
    ```

## Output

The script will output the repository names it's scanning. For each commit patch URL, it will display whether or not it contains any email addresses. If emails are found, they will be printed to the terminal.

## Important Notes

- This script is intended for educational purposes and should be used responsibly.
- Abusing this script to spam or harass individuals is against GitHub's terms of service and is unethical.
- The script adheres to the rate limits imposed by GitHub's API. Using a personal access token increases the rate limits, but please be mindful of the number of requests you are making.

## Contributing

Contributions to improve the script are welcome. Please fork the repository and submit a pull request with your suggested changes.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback regarding this script, please file an issue in the repository.

## Disclaimer

This script is provided "as is", without warranty of any kind. Use of this script is at your own risk.
