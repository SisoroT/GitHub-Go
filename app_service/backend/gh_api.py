import requests


def send_request(repo, author, endpoint):
    url = "https://api.github.com/search"
    if endpoint == "commits":
        url += "/commits"
        params = f"?q=repo:{repo}+author:{author}"
    else:
        url += "/issues"

        if endpoint == "pulls":
            params = f"?q=is:pr+repo:{repo}+author:{author}"
        elif endpoint == "reviews":
            params = f"?q=is:pr+repo:{repo}+reviewed-by:{author}"
        elif endpoint == "comments":
            params = f"?q=is:issue+repo:{repo}+commenter:{author}"
        else:
            return "Invalid endpoint."

    # github personal access token
    token = "YOUR_TOKEN_HERE"
    headers = {"Authorization": f"token {token}"}

    # send request
    response = requests.get(url + params, headers=headers)

    # return json response
    return response.json()


def main():
    # repo name
    repo = "CSC-4350-TR-SP2023/Team1"
    # person to lookup information for
    author = "SisoroT"

    # get and print total commits from author
    commits = send_request(repo, author, "commits")
    print("Commits:", commits["total_count"])

    # get and print total pull requests from author
    pulls = send_request(repo, author, "pulls")
    print("Pull requests:", pulls["total_count"])

    # get and print total pull requests reviewed by author
    reviews = send_request(repo, author, "reviews")
    print("Code reviews:", reviews["total_count"])

    # get and print total issues that have a comment from author
    comments = send_request(repo, author, "comments")
    print("Issue comments:", comments["total_count"])


if __name__ == "__main__":
    main()
