import datetime
import flask_mysqldb
from passlib.hash import sha256_crypt
import os
from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
#from dotenv import load_dotenv
#project_folder = os.path.expanduser('~/mysite')
#load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__, static_url_path='/static/')

app.config['MYSQL_HOST'] = 'localhost'#'victorf8.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'root'#'victorf8'
app.config['MYSQL_PASSWORD'] = ''#os.getenv("PASSWORD")
app.config['MYSQL_DB'] = 'cs_495'#'victorf8$cs_495'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cs_495'
#'mysql://victorf8:'+ os.getenv("PASSWORD") +'@victorf8.mysql.pythonanywhere-services.com/victorf8$cs_495'
app.config['SECRET_KEY'] = "halsdgkbrhjdfhaj320hdf"#os.getenv("SECRET_KEY")

mysql = flask_mysqldb.MySQL(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login = False

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if login:
        eventsList = []
        return render_template("events.html",login=login)
    return render_template("home.html", login=login)

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(user_id)
    return user

@app.route('/logout')
@login_required
def logout():
    global login
    logout_user()
    login = False
    return redirect(url_for('home'))

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    global login
    wrong = False
    wasSignUp = True
    if current_user.is_authenticated:
        return render_template('logout.html', login=login)
    if request.method == 'POST':
        name = request.form['name']
        if len(name) < 1:
            name = None
        user = Users(username=request.form['newusername'],
                     password=sha256_crypt.encrypt(request.form['newpassword']+app.config['SECRET_KEY']),
                     name=name)
        if Users.query.filter_by(username=user.username).first() == None:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            login = True
            return redirect(url_for('home'))
        else:
            wrong = True
    return render_template('login.html', login=login, wrong=wrong, wasSignUp=wasSignUp)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    global login
    wrong = False
    wasSignUp = False
    if current_user.is_authenticated:
        return render_template('logout.html', login=login)
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['username']).first()
        if user != None and sha256_crypt.verify(request.form['password']+app.config['SECRET_KEY'], user.password):
            login_user(user)
            login = True
            return redirect(url_for('home'))
        else:
            wrong = True
    return render_template('login.html', login=login, wrong=wrong, wasSignUp=wasSignUp)

@app.route('/view/<i>')
def view(i):
    return "view"

@app.route('/add', methods=['GET','POST'])
def add():
    if login:
        return "add"
    return redirect(url_for("sign_in"))

checkList = []

def setUpCheckList():
    global checkList
    cursor = mysql.connection.cursor()

    cursor.execute("select count(*) from sex")              # number of options that the sex could be
    count = cursor.fetchone()[0]
    checkList.append(count)

    cursor.execute("select count(*) from race")             # number of options that the race could be
    count = cursor.fetchone()[0]
    checkList.append(count)

    checkList.append(100)                                   # I don't think we'll have anyone older than 100

    cursor.execute("select count(*) from majors")           # number of options that the major could be
    count = cursor.fetchone()[0]
    checkList.append(count)
    checkList.append(count)                                 # a second time for the second major

    checkList.append(99)                                    # grad year should not be more than double digits

def checkString(s):
    global checkList
    try:
        data = s.split('/')
        if len(data) != 8:
            raise Exception

        for instance in data:                               # should all be (able to be) ints
            if not instance.isnumeric():
                raise Exception                             # 'raise Exception' just kicks code to the 'return False'

        stuID = data.pop(0)                                 # check format of studentID
        if len(stuID) != 6 or int(stuID) < 0:
            raise Exception

        intData = list(map(int,data))                       # for testing the value in the string
        code = intData.pop()

        if not checkList:                                   # one-time set up of values to test against
            setUpCheckList()
        for i in range(len(checkList)):                     # check values against constraints
            if not (0 < intData[i] <= checkList[i]):        # Taking advantage of python if statements
                raise Exception

        cursor = mysql.connection.cursor()                  # testing 'code' for getting an event
        # (see if 'code' is for real event)

        cursor.execute("select id from events where code = " + str(code) + ' and "'
                       + str(datetime.datetime.now().replace(microsecond=0))
                       + '" between startTime and endTime')
        if not cursor.fetchone():
            raise Exception

        return True
    except Exception:
        return False

def putInDatabase(s):
    cursor = mysql.connection.cursor()

    data = s.split('/')                                     # formatting the sql query
    code = data.pop()
    values = ""
    values += '"' + data[0] + '"'
    for i in range(1,len(data)):
        values += ', ' + data[i]
        # put event foreign key id in place of the code in the string
    cursor.execute("select id from events where code = " + str(code) + ' and "'
                   + str(datetime.datetime.now().replace(microsecond=0))
                   + '" between startTime and endTime')
    eventID = cursor.fetchone()[0]

    values += ', ' + str(eventID)
    sql = "INSERT INTO attendance (stuID, sex, race, age, major, major2, gradYear, event)" \
          " VALUES (" + values + ");"

    cursor.execute(sql)
    mysql.connection.commit()

@app.route('/submit-attendance', methods=['GET', 'POST'])
def attend():
    if request.method == 'POST':
        s = request.form['s']
        if checkString(s):
            putInDatabase(s)
            return 'success'
        else:
            return 'failure'
    return 'failure'

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     return render_template("test.html")

@app.errorhandler(404)
def err404(err):
    return render_template('error.html', err=err)

if __name__ == '__main__':
    app.run(host="0.0.0.0")