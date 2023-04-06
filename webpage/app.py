from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from backend.gh_api import send_request

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    searches = db.relationship("Search", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    repo = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Search('{self.username}','{self.repo}')"


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    # if the form is submitted
    if request.method == "POST":
        # get inputs from forms
        repo = request.form["repository"]
        author = request.form["username"]
        api_key = request.form["api_key"]

        # Store the API key in the session
        session["api_key"] = api_key

        template_params = {
            "repository": repo,
            "username": author,
            "api_key": api_key,
        }

        # if both repository and username have been filled out
        if repo and author and api_key:
            endpoints = ["commits", "pulls", "reviews", "comments"]
            counts = {}

            for endpoint in endpoints:
                # send request to github api
                response = send_request(repo, author, api_key, endpoint)

                is_error = isinstance(response, str)
                if is_error:
                    flash(response)
                    return render_template("home.html", **template_params)

                # store the total count for each endpoint
                counts[endpoint] = response["total_count"]

            user_not_contributor = sum(counts.values()) == 0
            if user_not_contributor:
                error = (
                    f'User "{author}" is not a contributor to the "{repo}" repository.'
                )
                flash(error)
                return render_template("home.html", **template_params)

            # if everything valid, redirect to the data page with info from API
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
            error = "Please provide a repository, username, and api key."
            flash(error)
            return render_template("home.html", **template_params)

    api_key = session.get("api_key", "")
    return render_template("home.html", api_key=api_key)


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
    return render_template("login.html", title="Login")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/forgot")
def forgot():
    return render_template("reset.html")


@app.route("/reset")
def reset():
    return render_template("reset_password.html")


if __name__ == "__main__":
    app.run(debug=True)
