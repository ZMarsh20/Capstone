from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.sqlite'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "hgbh9dfgh432bf98y4bnfd8oyvoubh4098fydsvojbnwereg98ydsvojbne"
login_manager = LoginManager(app)
login_manager.init_app(app)
login = False

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    clubs = db.relationship('Club', backref='user', lazy=True)

def loginStatusWord():
    if current_user.is_authenticated:
        return "Sign Out"
    return "Sign In"

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html",login=login)

@app.route('/add')
def add():
    Login = loginStatusWord()
    return render_template('add.html', login=Login)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

if __name__ == '__main__':
    app.run(host="0.0.0.0")