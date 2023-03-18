import requests


def send_request(repo, endpoint, author):
    if endpoint == "commits":
        url = f"https://api.github.com/repos/{repo}/{endpoint}"
        params = f"?author={author}&per_page=100"
    if endpoint == "pulls":
        url = "https://api.github.com/search/issues"
        params = f"?q=is:pull-request+author:{author}+repo:{repo}"

    # github personal access token
    token = "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"
    headers = {"Authorization": f"token {token}"}

    # send request
    response = requests.get(url + params, headers=headers)

    # return json response
    return response.json()


def main():
    # repo name
    repo = "CSC-4350-TR-SP2023/Team1"
    # repo = "baskerville/bspwm"
    # person to lookup information for
    author = "SisoroT"
    # author = "Stebalien"

    # get all commits from author
    commits = send_request(repo, "commits", author)
    # print total commits for author
    print(len(commits))

    # get all pull requests from author
    pulls = send_request(repo, "pulls", author)
    # print total pull requests for author
    print(pulls["total_count"])


if __name__ == "__main__":
    main()
