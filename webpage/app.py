from flask import Flask, render_template, url_for, redirect, request, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db, User, Search
from backend.gh_api import send_request, xor_encrypt_decrypt

app = Flask(__name__)
app.secret_key = "super_secret_key"
# encrypt the API key with a different key
SECRET_KEY = "another_really_super_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# initialize the database
db.init_app(app)
# load the database
with app.app_context():
    db.create_all()


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    # if the form is submitted
    if request.method == "POST":
        # get inputs from forms
        repo = request.form["repository"]
        author = request.form["username"]
        api_key = request.form["api_key"]

        # scramble the API key
        scrambled_api_key = xor_encrypt_decrypt(api_key, SECRET_KEY)

        if g.user:
            # Update the scrambled API key in the database for logged-in users
            g.user.api_key = scrambled_api_key
            db.session.commit()
        else:
            # Store the scrambled API key in the session for non-logged-in users
            session["api_key"] = scrambled_api_key

        template_params = {
            "repository": repo,
            "username": author,
            "api_key": api_key,
        }

        # if both repository and username have been filled out
        if repo and author and api_key:
            return search(repo, author, api_key, template_params)
        else:
            error = "Please provide a repository, username, and api key."
            flash(error)

    # Load API key from the database and unscramble if logged in
    if g.user and g.user.api_key:
        api_key = xor_encrypt_decrypt(g.user.api_key, SECRET_KEY)
    else:
        # Load API key from the session and unscramble if not logged in
        scrambled_api_key = session.get("api_key", "")
        api_key = xor_encrypt_decrypt(scrambled_api_key, SECRET_KEY)

    return render_template("home.html", api_key=api_key)


@app.route("/data/<path:repository>/<string:username>")
def data(repository, username):
    # collect extra information from url arguments
    commits = request.args.get("commits")
    pulls = request.args.get("pulls")
    reviews = request.args.get("reviews")
    comments = request.args.get("comments")

    # get search history if logged in
    search_history = None
    if g.user:
        search_history = Search.query.filter_by(user_id=g.user.id).all()

    return render_template(
        "data.html",
        repository=repository,
        username=username,
        commits=commits,
        pulls=pulls,
        reviews=reviews,
        comments=comments,
        search_history=search_history,
    )


@app.route("/rerun_search/<path:repo>/<string:username>")
def rerun_search(repo, username):
    # Load API key from the database and unscramble if logged in
    if g.user and g.user.api_key:
        api_key = xor_encrypt_decrypt(g.user.api_key, SECRET_KEY)
    else:
        # Load API key from the session and unscramble if not logged in
        scrambled_api_key = session.get("api_key", "")
        api_key = xor_encrypt_decrypt(scrambled_api_key, SECRET_KEY)

    if not api_key:
        flash("No API key found. Please perform a search on the home page.")
        return redirect(url_for("home"))

    return search(repo, username, api_key)


def search(repo, username, api_key, template_params=None):
    endpoints = ["commits", "pulls", "reviews", "comments"]
    counts = {}

    # if template_params is not provided,
    # create an empty dictionary to avoid errors
    if template_params is None:
        template_params = {}

    for endpoint in endpoints:
        # send request to github api
        response = send_request(repo, username, api_key, endpoint)

        is_error = isinstance(response, str)
        if is_error:
            flash(response)
            return render_template("home.html", **template_params)

        # store the total count for each endpoint
        counts[endpoint] = response["total_count"]

    user_not_contributor = sum(counts.values()) == 0
    if user_not_contributor:
        error = f'User "{username}" is not a contributor to the "{repo}" repository.'
        flash(error)
        return render_template("home.html", **template_params)

    # save search to database if logged in
    if g.user:
        user = User.query.filter_by(username=session["username"]).first()
        if user:
            existing_search = Search.query.filter(
                Search.username.ilike(username),
                Search.repo.ilike(repo),
                Search.user_id == user.id,
            ).first()
            if not existing_search:
                search = Search(username=username, repo=repo, user_id=user.id)
                db.session.add(search)
                db.session.commit()

    # if everything valid, redirect to the data page with info from API
    return redirect(
        url_for(
            "data",
            repository=repo,
            username=username,
            commits=counts["commits"],
            pulls=counts["pulls"],
            reviews=counts["reviews"],
            comments=counts["comments"],
        )
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    # if logged in, redirect to home page
    if g.user:
        return redirect(url_for("home"))

    # if username and password exist in DB, log in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = username
            return redirect(url_for("home"))
        # if user or password is incorrect/does not exist
        else:
            flash("Invalid username or password.")

    return render_template("login.html", title="Login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # if passwords do not match flash error
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("signup"))

        # if username already exists flash error
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already taken.")
            return redirect(url_for("signup"))

        # if valid, hash password and add all info to database
        hashed_password = generate_password_hash(password, method="sha256")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # alert user that account was created successfully
        flash("Account created successfully.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/forgot")
def forgot():
    return render_template("reset.html")


@app.route("/reset")
def reset():
    return render_template("reset_password.html")


# NOTE: Testing route to view all entries in the database
@app.route("/db")
def show_db():
    users = User.query.all()
    search_histories = Search.query.all()
    return render_template(
        "show_db.html", users=users, search_histories=search_histories
    )


if __name__ == "__main__":
    app.run(debug=True)
