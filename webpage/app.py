from flask import Flask, render_template, url_for, request, redirect
from login import searchLogin
from register import createRegister

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if 'login' in request.form:
            thisUser = request.form.get('username')
            thisPass = request.form.get('password')
            searchLogin(thisUser, thisPass) 
            return render_template('home.html')
        if 'register' in request.form:
            thisUser = request.form.get('username')
            thisPass = request.form.get('password')
            createRegister(thisUser, thisPass) 
            return render_template('home.html')
    return render_template('login.html', title='Login')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/reset_password")
def reset():
    return render_template('reset_password.html')


@app.route("/reset")
def forgot():
    return render_template('reset.html')


@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/home_test", methods=["POST", "GET"])
def home_test():
    if request.method == "POST":
        if 'login' in request.form:
            thisUser = request.form.get('username')
            thisPass = request.form.get('password')
            searchLogin(thisUser, thisPass) 
            return render_template('home.html')
        if 'register' in request.form:
            thisUser = request.form.get('username')
            thisPass = request.form.get('password')
            createRegister(thisUser, thisPass) 
            return render_template('home.html')
    return render_template('data.html')



if __name__ == "__main__":
    app.run(debug=True)
