from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/login")
def login():
    return render_template('login.html', title='Login')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/resetPassword")
def reset():
    return render_template('resetPassword.html')


@app.route("/reset")
def forgot():
    return render_template('reset.html')


@app.route("/data")
def data():
    return render_template('data.html')


if __name__ == "__main__":
    app.run(debug=True)
