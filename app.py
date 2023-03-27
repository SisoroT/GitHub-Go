from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def homepage():
    return render_template('mainPage.html', title='Home')
