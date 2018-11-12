# GitHubStarsHistory: GitHub Stars History Downloader

GitHubStarsHistory is a data downloader that uses the GitHub API in order to calculate the stars information for a given GitHub
repository since its creation. The tool uses the GitHub API v3, for which more information can be found [here](https://developer.github.com/v3/).

Prerequisites
-------------
The python library requirements are available in file `requirements.txt` and may be installed using
the command:
```
pip install -r requirements.txt
```

To run this tool, you must have a GitHub account. Also, you must create a GitHub personal access token
(instructions to create one are available [here](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/))
and set it in file `properties.py`.

Executing the tool
------------------
- **CLI Usage**

To run the tool, one must first correctly assign the properties in file `properties.py`.
After that, the tool can be executed by running the following command: 
```
python starsHistoryCalculator.py [github_repo_url]
```

where `github_repo_url` must be replaced by a GitHub repo URL (e.g. `https://github.com/pubnub/java`)

The parameters that need to be set in the `properties.py` are the following:
- `GitHubAuthToken`: your GitHub personal access token (instructions to get one are available [here](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/))
- `ResultsDir`: the path to the directory in your system, where you want to save the results

- **Embed into your code**

You can embed the tool into your code by using the following commands:

```python
from starsHistoryCalculator import GitHubStarsHistory

# Instantiate the stars data calculator
starsHistory = GitHubStarsHistory()

# Get the stars information
info = starsHistory.download_stargazers('pubnub/java')

# View stars info
import json
print(json.dumps(info, indent=3, sort_keys=True))
```
