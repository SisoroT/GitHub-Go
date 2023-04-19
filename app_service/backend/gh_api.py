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

    limit_exceeded_msg = "API rate limit exceeded for user ID"
    if "message" in json_response and limit_exceeded_msg in json_response["message"]:
        return "API limit exceeded. Please wait 60 seconds and try again."

    # check for invalid repo or username
    if "total_count" not in json_response:
        return "Invalid repository or username. Please check the input and try again."

    return json_response


def xor_encrypt_decrypt(data, key):
    key_len = len(key)
    return "".join(chr(ord(data[i]) ^ ord(key[i % key_len])) for i in range(len(data)))


def main():
    # repo name
    repo = "CSC-4350-TR-SP2023/Team1"
    # person to lookup information for
    author = "SisoroT"

    api_key = "YOUR_TOKEN_HERE"
    endpoints = ["commits", "pulls", "reviews", "comments"]

    # get and print the totals for each endpoint by author
    for endpoint in endpoints:
        response = send_request(repo, author, api_key, endpoint)
        is_error = isinstance(response, str)
        if is_error:
            print(response)
        else:
            print(f"{endpoint}: {response['total_count']}")


if __name__ == "__main__":
    main()
