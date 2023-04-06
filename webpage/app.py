from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(60), nullable=False)
    searches = db.relationship('Search', backref='user',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    repo = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"Search('{self.username}','{self.repo}')"

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


@app.route("/reset_password")
def reset():
    return render_template('reset_password.html')


@app.route("/reset")
def forgot():
    return render_template('reset.html')


@app.route("/data")
def data():
    return render_template('data.html')


if __name__ == "__main__":
    app.run(debug=True)

