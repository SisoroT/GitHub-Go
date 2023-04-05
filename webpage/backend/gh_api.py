import requests
from requests.exceptions import RequestException


def send_request(repo: str, author: str, api_key: str, endpoint: str):
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
    token = api_key
    headers = {"Authorization": f"token {token}"}

    try:
        # send request
        response = requests.get(url + params, headers=headers)
        # decode json response
        json_response = response.json()
    except RequestException as e:
        return f"Request error: {e}"
    except ValueError:
        return "Error decoding JSON response."

    # check for bad credentials
    if "message" in json_response and json_response["message"] == "Bad credentials":
        return "Invalid personal access token."

    return json_response


def main():
    # repo name
    repo = "CSC-4350-TR-SP2023/Team1"
    # person to lookup information for
    author = "SisoroT"

    api_key = "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"

    # get and print total commits from author
    commits = send_request(repo, author, api_key, "commits")
    print("Commits:", commits["total_count"])

    # get and print total pull requests from author
    pulls = send_request(repo, author, api_key, "pulls")
    print("Pull requests:", pulls["total_count"])

    # get and print total pull requests reviewed by author
    reviews = send_request(repo, author, api_key, "reviews")
    print("Code reviews:", reviews["total_count"])

    # get and print total issues that have a comment from author
    comments = send_request(repo, author, api_key, "comments")
    print("Issue comments:", comments["total_count"])


if __name__ == "__main__":
    main()
