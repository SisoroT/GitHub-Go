import requests


def send_request(repo, endpoint, author):
    url = f"https://api.github.com/repos/{repo}/{endpoint}"
    params = {"author": author}

    if endpoint == "commits":
        params.update({"per_page": 100})
    if endpoint == "pulls":
        params.update({"state": "all", "per_page": 100})

    # github personal access token
    token = "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"
    headers = {"Authorization": f"token {token}"}

    # send request
    response = requests.get(url, params=params, headers=headers)

    # return json response
    return response.json()


def main():
    # repo name
    repo = "baskerville/bspwm"
    # person to lookup information for
    author = "Stebalien"
    repo = "CSC-4350-TR-SP2023/Team1"
    author = "SisoroT"

    # get all commits from author
    commits = send_request(repo, "commits", author)
    # print total commits for author
    print(len(commits))

    # get all pull requests from author
    pulls = send_request(repo, "pulls", author)
    # print total pull requests for author
    print(len(pulls))


if __name__ == "__main__":
    main()
