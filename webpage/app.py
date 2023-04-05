from flask import Flask, render_template, url_for, redirect, request, flash
from backend.gh_api import send_request

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    error = None

    # if the form is submitted
    if request.method == "POST":
        repo = request.form["repository"]
        author = request.form["username"]

        # if both repository and username have been filled out
        if repo and author:
            endpoints = ["commits", "pulls", "reviews", "comments"]
            counts = {}

            for endpoint in endpoints:
                try:
                    response = send_request(repo, author, endpoint)
                except Exception as e:
                    flash(str(e))
                    return render_template(
                        "home.html", repository=repo, username=author
                    )

                # if total_count isn't in the response, the repo or username is invalid
                if "total_count" not in response:
                    error = "Invalid repository or username. Please check the input and try again."
                    flash(error)
                    return render_template(
                        "home.html", repository=repo, username=author
                    )

                counts[endpoint] = response["total_count"]

            user_not_contributor = sum(counts.values()) == 0
            if user_not_contributor:
                error = (
                    f'User "{author}" is not a contributor to the "{repo}" repository.'
                )
                flash(error)
                return render_template("home.html", repository=repo, username=author)

            # if the repo and username are valid, redirect to the data page
            # and pass all the information received from the API
            return redirect(
                url_for(
                    "data",
                    repository=repo,
                    username=author,
                    commits=counts["commits"],
                    pulls=counts["pulls"],
                    reviews=counts["reviews"],
                    comments=counts["comments"],
                )
            )
        else:
            error = "Please provide both repository and username."
            flash(error)
            return render_template("home.html", repository=repo, username=author)

    return render_template("home.html")


@app.route("/data/<path:repository>/<string:username>")
def data(repository, username):
    # collect extra information from url arguments
    commits = request.args.get("commits")
    pulls = request.args.get("pulls")
    reviews = request.args.get("reviews")
    comments = request.args.get("comments")

    return render_template(
        "data.html",
        repository=repository,
        username=username,
        commits=commits,
        pulls=pulls,
        reviews=reviews,
        comments=comments,
    )


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/forgot")
def forgot():
    return render_template("forgot_password.html")


@app.route("/reset")
def reset():
    return render_template("reset_password.html")


if __name__ == "__main__":
    app.run(debug=True)
