from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("main_page.html")


@app.route("/data")
def data():
    return render_template("data_page.html")


@app.route("/login")
def login():
    return render_template("login_page.html")


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
