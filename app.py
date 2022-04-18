import flask_mysqldb
import random
import time
from datetime import datetime
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, url_for, redirect, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
#import os
#from dotenv import load_dotenv
#project_folder = os.path.expanduser('~/mysite')
#load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__, static_url_path='/static/')

app.config['MYSQL_HOST'] = 'localhost'#'victorf8.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'root'#'victorf8'
app.config['MYSQL_PASSWORD'] = ''#os.getenv("PASSWORD")
app.config['MYSQL_DB'] = 'cs_495'#'victorf8$cs_495'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME'] = 'spamm.western@gmail.com'
app.config['MAIL_PASSWORD'] = '&CS495capstone&'#os.getenv("PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cs_495'
#'mysql://victorf8:'+ os.getenv("PASSWORD") +'@victorf8.mysql.pythonanywhere-services.com/victorf8$cs_495'
app.config['SECRET_KEY'] = "halsdgkbrhjdfhaj320hdf"#os.getenv("SECRET_KEY")

mysql = flask_mysqldb.MySQL(app)
db = SQLAlchemy(app)
mail = Mail(app)

#os.environ["TZ"] = "America/Denver"
#time.tzset()

login_manager = LoginManager(app)
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40))
    events = db.relationship('Events', backref='users', lazy=True)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(45), unique=True, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))


def timeformat(s):
    return s.replace("T"," ") + ":00"

def codeTaken(event):
    codes = Events.query.filter_by(code=event.code)
    for code in codes:
        if str(code.startTime) <= event.startTime <= str(code.endTime) \
            or str(code.startTime) <= event.endTime <= str(code.endTime):
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    session['delete'] = session['addwrong'] = session['addwrong2'] = False
    if current_user.is_authenticated:
        if request.method == 'POST':
            event = Events( event=request.form['eName'],
                            startTime=timeformat(request.form['start']),
                            endTime=timeformat(request.form['end']),
                            code=request.form['code'], user=current_user.id)
            if (Events.query.filter_by(event=event.event).first() is None and "REMOVED" not in event.event) or session['update']:
                if codeTaken(event):
                    if session['update']:
                        temp = Events.query.filter_by(event=event.event).first()
                        temp.startTime = event.startTime
                        temp.endTime = event.endTime
                        temp.code = event.code
                    else:
                        db.session.add(event)
                    db.session.commit()
                    session['update'] = False
                else:
                    session['addwrong2'] = True
                    return '<script>document.location.href = document.referrer</script>'
            else:
                session['addwrong'] = True
                return '<script>document.location.href = document.referrer</script>'
        eventsList = Events.query.filter_by(user=current_user.id).all()
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template("events.html", eventsList=eventsList, currentTime=currentTime)
    return render_template("home.html", login=(not current_user.is_authenticated))

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(user_id)
    return user

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/e-auth',methods=['GET','POST'])
def emailAuth():
    if request.method == "POST":
        if request.form["pword"] == str(session['code']) and (time.time()-session['timer']) < (10*60):
            user = Users(username=session['tmpUser.username'],
                         password=session['tmpUser.password'],
                         name=session['tmpUser.name'])
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session.pop('tmpUser.username',None)
            session.pop('tmpUser.password',None)
            session.pop('tmpUser.name',None)
            session.pop('code', None)
            return redirect(url_for('home'))
    return render_template('emailAuth.html', wrong=True)

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    wrong = False
    wasSignUp = True
    if current_user.is_authenticated:
        return render_template('logout.html', login=(not current_user.is_authenticated))
    if request.method == 'POST':
        name = request.form['name']
        if len(name) < 1:
            name = None
        user = Users(username=request.form['newusername'],
                     password=sha256_crypt.encrypt(request.form['newpassword']+app.config['SECRET_KEY']),
                     name=name)
        if Users.query.filter_by(username=user.username).first() is None:
            if "@" in user.username and "western.edu" in user.username.split('@')[-1]:
                session['code'] = random.randint(100000000,999999999)
                session['timer'] = time.time()
                msg = Message('Email Confirmation Code', recipients=[user.username])
                msg.body = 'Here is your confirmation code: ' + str(session['code'])
                mail.send(msg)
                session['tmpUser.username'] = user.username
                session['tmpUser.password'] = user.password
                session['tmpUser.name'] = user.name
                return render_template('emailAuth.html', login=(not current_user.is_authenticated))
        wrong = True
    return render_template('login.html', login=(not current_user.is_authenticated), wrong=wrong, wasSignUp=wasSignUp)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    wrong = False
    wasSignUp = False
    if current_user.is_authenticated:
        return render_template('logout.html', login=(not current_user.is_authenticated))
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['username']).first()
        if user is not None and sha256_crypt.verify(request.form['password']+app.config['SECRET_KEY'], user.password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            wrong = True
    return render_template('login.html', login=(not current_user.is_authenticated), wrong=wrong, wasSignUp=wasSignUp)

@app.route('/view/<i>', methods=['GET','POST'])
def view(i):
    sexs = {}
    races = {}
    majors = {}
    housings = {}
    grads = {}
    if request.method == "POST":
        results = """select sex.sex as "Sex", race.race as "Ethnicity", age as "Age", gradYear as "Grad Year", 
                maj.major as "Major", min.major as "Minor", maj2.major as "Second Major", min2.major as "Second Minor", 
                case when program=0 then "undergrad" else "graduate" end as "Program", 
                case when housing=0 then "off" else "on" end as "Housing", 
                case when transfer=0 then "is not" else "is" end as "Transferer", 
                case when latinx=0 then "is not" else "is" end as "Latinx", access as "Access" from attendance 
                join sex on attendance.sex=sex.id 
                join race on attendance.race=race.id
                join majors maj on attendance.major = maj.id
                join majors min on attendance.minor = min.id
                join majors maj2 on attendance.major2 = maj2.id
                join majors min2 on attendance.minor2 = min2.id;"""
        render_template('results.html', results=results)
    return render_template('view.html', eventNum=i,
                           sexs=sexs, races=races, majors=majors, housings=housings, grads=grads)

@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    session['update'] = False
    return render_template('add.html', addwrong=session['addwrong'], addwrong2=session['addwrong2'])

@app.route('/update/<i>', methods=['GET','POST'])
@login_required
def update(i):
    session['update'] = True
    event = Events.query.filter_by(id=i).first()
    if str(event.startTime) <= datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        abort(401)
    return render_template('update.html', event=event, addwrong2=session['addwrong2'])

@app.route('/delete/<i>', methods=['GET','POST'])
@login_required
def delete(i):
    if session['delete']:
        event = Events.query.filter_by(id=i).first()
        session['delete'] = False
        if datetime.now().strftime("%Y-%m-%d %H:%M:%S") < str(event.startTime):
            db.session.delete(event)
        else:
            event.event = "REMOVED BY USER " + event.user
            event.user = event.code = 0
            event.endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return redirect(url_for("home"))
    else:
        session['delete'] = True
        return '<script src="/static/delete.js"></script><script>deleter(' + i + ')</script>'

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
    for _ in range(4):
        checkList.append(count)                             # four times for (major, minor, major2, minor2)

    checkList.append(99)                                    # grad year should not be more than double digits

    for _ in range(4):
        checkList.append(1)                                 # four booleans (program, housing(on/off), transfer, latinx)

def checkString(s):
    global checkList
    try:
        data = s.split('/')
        if len(data) != len(checkList)+3:
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
                       + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                   + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                   + '" between startTime and endTime')
    eventID = cursor.fetchone()[0]

    values += ', ' + str(eventID)
    sql = "INSERT INTO attendance (stuID, sex, race, age, major, minor, major2, minor2," \
          " gradYear, program, housing, transfer, latinx, event, access)" \
          " VALUES (" + values + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ");"

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

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html")

@app.errorhandler(404)
def err404(err):
    return render_template('error.html', err=err, login=(not current_user.is_authenticated))

@app.errorhandler(401)
def err401(err):
    return render_template('error.html', err=err, login=(not current_user.is_authenticated))

if __name__ == '__main__':
    app.run()