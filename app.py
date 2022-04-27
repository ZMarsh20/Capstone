import time
import MySQLdb
from random import randint
from datetime import datetime
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect, abort, session
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from flask_qrcode import QRcode
import flask_mysqldb
#import os
#from dotenv import load_dotenv
#project_folder = os.path.expanduser('~/mysite')
#load_dotenv(os.path.join(project_folder, '.env'))

    # Comments up here at the beginning are necessary for pythonanywhere.
    # Comments behind strings are to replace them.

app = Flask(__name__, static_url_path='/static/')

app.config['MYSQL_HOST'] = 'localhost'#'victorf8.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'root'#'victorf8'
app.config['MYSQL_PASSWORD'] = ''#os.getenv("PASSWORD")
app.config['MYSQL_DB'] = 'cs_495'#'victorf8$cs_495'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME'] = 'westerncapstone@gmail.com'
app.config['MAIL_PASSWORD'] = ''#os.getenv("PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cs_495'
#'mysql://victorf8:'+ os.getenv("PASSWORD") +'@victorf8.mysql.pythonanywhere-services.com/victorf8$cs_495'
app.config['SECRET_KEY'] = "halsdgkbrhjdfhaj320hdf"#os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

mysql = flask_mysqldb.MySQL(app)
db = SQLAlchemy(app)
mail = Mail(app)
QRcode(app)

#os.environ["TZ"] = "America/Denver"                # Make it not UTC.
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

def safeCursor():
    try:
        cursor = mysql.connection.cursor()
    except (AttributeError, MySQLdb.OperationalError):      # If connection was closed, open it so no error.
        mysql.connect()
        cursor = mysql.connection.cursor()
    return cursor

sexQuery = ()
raceQuery = ()
majorQuery = ()
checkList = []
bools = 5
@app.before_first_request                                   # Runs on startup (essentially).
def setQueries():
    global sexQuery,raceQuery,majorQuery
    global checkList, bools
    cursor = safeCursor()
    cursor.execute("select sex from sex order by id")       # Set up three common queries to just do once.
    sexQuery = cursor.fetchall()
    cursor.execute("select race from race order by id")     # Sex race and major are used a couple times lower.
    raceQuery = cursor.fetchall()
    cursor.execute("select major from majors order by id")  # These are fine as globals since they shouldn't change.
    majorQuery = cursor.fetchall()


    checkList.append(len(sexQuery))                         # Number of options that the sex could be.

    checkList.append(len(raceQuery))                        # Number of options that the race could be.

    checkList.append(100)                                   # I don't think we'll have anyone older than 100.

    for _ in range(4):                                      # Four times for (major, minor, major2, minor2)
        checkList.append(len(majorQuery))                   # number of options that the major could be.

    checkList.append(99)                                    # Grad year should not be more than double digits.

    for _ in range(bools):                                  # Five booleans (program, housing(on/off),
        checkList.append(1)                                 # transfer, latinx, lgbtq).

def timeformat(s):
    return s.replace("T"," ") + ":00"                       # Fix weird syntax from form.

def checkMaxEvents(event):
    max = 4
    cursor = safeCursor()
    sql = "select count(*) from events where user = " + str(current_user.id) \
    + ' and (startTime between "' + str(event.startTime) + '" and "' + str(event.endTime) \
    + '" or endTime between "' + str(event.startTime) + '" and "' + str(event.endTime) \
    + '" or "' + str(event.startTime) + '" between startTime and endTime)'
                                                            # Last bit for being contained entirely within other event.
    if session['update']:                                   # Could add this regardless since without updating
        sql += ' and event != "' + event.event + '"'        # the name wouldn't be present therefore wouldn't affect
    cursor.execute(sql)                                     # outcome but easier to read.
    if cursor.fetchone()[0] > max:
        return True
    return False

def codeTaken(event):
    codes = Events.query.filter_by(code=event.code)         # Checking time overlaps.
    for code in codes:
        if str(code.event) == str(event.event) and int(code.code) == int(event.code):  # Only possible in updating. Same code is allowed
            continue                                    # if update now overlaps it will still be caught by the next code.
        if str(code.startTime) <= event.startTime <= str(code.endTime) \
                or str(code.startTime) <= event.endTime <= str(code.endTime) \
                or event.startTime < str(code.startTime) < event.endTime:
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    session['delete'] = False                                               # Clean up when home.
    session['addwrong'] = session['addwrong2'] = session['addwrong3'] = False  
    if current_user.is_authenticated:                                       # Home is event.html when logged in.
        if request.method == 'POST':                                        # Posted from add page so checking to add
            event = Events( event=request.form['eName'],                    # new event.
                            startTime=timeformat(request.form['start']),
                            endTime=timeformat(request.form['end']),
                            code=request.form['code'], user=current_user.id)
            if checkMaxEvents(event):
                session['addwrong3'] = True                                 # addwrong3 is too many events.
                return '<script>document.location.href = document.referrer</script>'
            if (Events.query.filter_by(event=event.event).first() is None
                and "REMOVED" not in event.event) or session['update']:     # Ff "REMOVED" is in their event, it could cause
                if codeTaken(event):                                        # problems with overlap in deleting.
                    if session['update']:
                        temp = Events.query.filter_by(event=event.event).first()
                        temp.startTime = event.startTime
                        temp.endTime = event.endTime
                        temp.code = event.code
                    else:                                                   # If updating, it's much more involved than
                        db.session.add(event)                               # just adding with ORM.
                    db.session.commit()
                    session['update'] = False
                else:                                                       # addwrong2 is code taken.
                    session['addwrong2'] = True
                    return '<script>document.location.href = document.referrer</script>'  # Simple "back" return.
            else:
                session['addwrong'] = True                                  # addwrong is event name invalid.
                return '<script>document.location.href = document.referrer</script>'
        eventsList = Events.query.filter_by(user=current_user.id).all()
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")          # Display all events on home page.
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
    if current_user.is_authenticated:
        return render_template('logout.html', login=(not current_user.is_authenticated))
    if request.method == "POST":                            # Check code and within 10mins time to verify.
        if request.form["pword"] == str(session['code']) and (time.time()-session['timer']) < (10*60):
            user = Users(username=session['tmpUser.username'],
                         password=session['tmpUser.password'],
                         name=session['tmpUser.name'])
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session.pop('tmpUser.username',None)            # No need for these after this route.
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
        if len(name) < 1:                           # name = None instead of "".
            name = None
        user = Users(username=request.form['newusername'],
                     password=sha256_crypt.encrypt(request.form['newpassword']+app.config['SECRET_KEY']),
                     name=name)
        if Users.query.filter_by(username=user.username).first() is None:               # Already a user?
            if "@" in user.username and "western.edu" in user.username.split('@')[-1]:  # Western emails only.
                session['code'] = randint(100000000,999999999)                   # The verification code.
                session['timer'] = time.time()                                          # Ten min timer.
                msg = Message('Email Confirmation Code', recipients=[user.username])    # Email message boiler plate.
                msg.body = 'Here is your confirmation code: ' + str(session['code'])
                mail.send(msg)
                session['tmpUser.username'] = user.username                              # Carry new user to email-auth.
                session['tmpUser.password'] = user.password
                session['tmpUser.name'] = user.name
                return render_template('emailAuth.html', login=(not current_user.is_authenticated))
        wrong = True
    return render_template('login.html', login=(not current_user.is_authenticated), wrong=wrong, wasSignUp=wasSignUp)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    wrong = wasSignUp = False
    if current_user.is_authenticated:
        return render_template('logout.html', login=(not current_user.is_authenticated))
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['username']).first()    # Check username then password.
        if user is not None and sha256_crypt.verify(request.form['password']+app.config['SECRET_KEY'], user.password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            wrong = True
    return render_template('login.html', login=(not current_user.is_authenticated), wrong=wrong, wasSignUp=wasSignUp)

def permission(i):
    eventUser = Events.query.filter_by(id=i).first()            # Verify that event id belongs to user.
    if eventUser is None or eventUser.user != current_user.id:
        abort(401)
    return eventUser

def fillView(y):
    x = {0:"any"}
    for i in range(len(y)):             # "/" for races to cut off early.
        if "/" in y[i][0]:              # No need to search for mixed ethnicities alone.
            break
        x[i+1] = y[i][0]                # i+1 offsets the 0 choice for any.
    return x

@app.route('/view/<i>', methods=['GET','POST'])
@login_required
def view(i):
    global sexQuery,raceQuery,majorQuery
    cursor = safeCursor()
    event = permission(i).event
    if request.method == "POST":        # A lovely query for all filtered data.
        resultsQuery = """
            select attendance.stuID, sex.sex, race.race, age, gradYear, 
            maj.major, min.major, maj2.major, min2.major, 
            case when program=0 then "undergrad" else "graduate" end, 
            case when housing=0 then "off" else "on" end, 
            case when transfer=0 then "is not" else "is"end, 
            case when latinx=0 then "is not" else "is" end,
            case when lgbtq=0 then "is not" else "is" end,
            access as "Access" from attendance 
            join sex on attendance.sex=sex.id 
            join race on attendance.race=race.id
            join majors maj on attendance.major = maj.id
            join majors min on attendance.minor = min.id
            join majors maj2 on attendance.major2 = maj2.id
            join majors min2 on attendance.minor2 = min2.id """
        s = ""
        if request.form['sex'] != '0':
            s += " and attendance.sex = " + request.form['sex']
        if request.form['race'] != 'any':
            s += " and race.race like '%" + request.form['race'] + "%'"     # %% so 'asian' also selects part asian peoples.
        if request.form['major1'] != '0':
            s += " and attendance.major = " + request.form['major1']
        if request.form['minor1'] != '0':
            s += " and minor = " + request.form['minor1']                   # Messy and gross but I think the only way to
        if request.form['major2'] != '0':                                   # really do these. Similar pattern but different
            s += " and major2 = " + request.form['major2']                  # data for the query.
        if request.form['minor2'] != '0':
            s += " and minor2 = " + request.form['minor2']
        if request.form['grad'] != '0':
            s += " and program = " + str(int(request.form['grad']) - 1)     # These two are boolean values but with option
        if request.form['housing'] != '0':                                  # to see either as well as both.
            s += " and housing = " + str(int(request.form['housing']) - 1)
        if request.form.get('latinx') is not None:                          # These three are booleans where only check
            s += " and latinx = 1"                                          # "both" or "true". no need for only "not true"
        if request.form.get('transfer') is not None:
            s += " and transfer = 1"
        if request.form.get('lgbtq') is not None:
            s += " and lgbtq = 1"
        if request.form['gradStart'] != "":
            if request.form['gradStart'] == request.form['gradEnd']:        # If they're equal no need for between.
                s += " and gradYear = " + request.form['gradStart']
            else:
                s += " and gradYear between " + request.form['gradStart'] + " and " + request.form['gradEnd']
        if request.form['ageStart'] != "":
            if request.form['ageStart'] == request.form['ageEnd']:
                s += " and age = " + request.form['ageStart']
            else:
                s += " and age between " + request.form['ageStart'] + " and " + request.form['ageEnd']

        resultsQuery += "where attendance.event = " + str(i)
        resultsQuery += s                           # If no filters s = "" otherwise it will include the 'and'.
        resultsQuery += """ group by attendance.stuID
                        order by attendance.access desc limit 100"""
                                                    # group by -> no duplicates.
        cursor.execute(resultsQuery)                # order by -> I think it does regardless but why not add it.
        results = cursor.fetchall()                 # limit 100 -> very necessary for efficient querying.
        return render_template('results.html', eventNum=i, results=results)

    sexs = fillView(sexQuery)
    races = fillView(raceQuery)
    majors = fillView(majorQuery)                       # All selections for form.
    housings = {0:"Both",1:"Off Campus",2:"On Campus"}
    grads = {0:"Both",1:"Undergraduate",2:"Graduate"}
    return render_template('view.html', eventNum=i, event=event,
                           sexs=sexs, races=races, majors=majors, housings=housings, grads=grads)

@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    session['update'] = False
    addwrong = session['addwrong']
    addwrong2 = session['addwrong2']
    addwrong3 = session['addwrong3']
    session['addwrong'] = session['addwrong2'] = session['addwrong3'] = False
    return render_template('add.html', addwrong=addwrong, addwrong2=addwrong2, addwrong3=addwrong3)

@app.route('/update/<i>', methods=['GET','POST'])
@login_required
def update(i):
    event = permission(i)
    if str(event.startTime) <= datetime.now().strftime("%Y-%m-%d %H:%M:%S"):  # Can't update if ongoing (or past).
        abort(401)
    session['update'] = True
    addwrong2 = session['addwrong2']
    addwrong3 = session['addwrong3']
    session['addwrong2'] = session['addwrong3'] = False
    return render_template('add.html', event=event, update=True, addwrong2=addwrong2, addwrong3=addwrong3)

@app.route('/delete/<i>', methods=['GET','POST'])
@login_required
def delete(i):
    permission(i)
    if session['delete']:
        event = Events.query.filter_by(id=i).first()
        session['delete'] = False
        if datetime.now().strftime("%Y-%m-%d %H:%M:%S") < str(event.startTime):  # Can't delete if ongoing (or past)
            db.session.delete(event)
        else:                                                                    # Special syntax to know who owned
            event.event = "REMOVED BY USER " + str(event.user)                   # event before deletion.
            event.user = event.code = 0                                          # Now only accessible to those with
            event.endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")         # access to database directly (admin).
        db.session.commit()
        return redirect(url_for("home"))
    else:
        session['delete'] = True                                                 # Double check on deleting.
        return '<script src="/static/delete.js"></script><script>deleter(' + i + ')</script>'  # Kinda ugly but didn't
                                                                                        # want to make whole new html.

def checkString(s):
    global checkList
    cursor = safeCursor()
    try:
        data = s.split('/')
        if len(data) != len(checkList)+2:                   # Plus 2 because of stuID and code.
            raise Exception

        for instance in data:                               # Should all be (able to be) ints.
            if not instance.isnumeric():
                raise Exception                             # 'raise Exception' just kicks code to the 'return False'.

        stuID = data.pop(0)                                 # Check format of studentID.
        if len(stuID) != 6 or int(stuID) < 0:
            raise Exception
        for i in stuID:
            if not i.isnumeric():                           # Handling 1e200 or 0x123 and other cases.
                raise Exception

        intData = list(map(int,data))                       # For testing the value in the string.
        code = intData.pop()

        for i in range(len(checkList)):                     # Check values against constraints
            if i >= len(checkList) - bools:                 # these are the boolean values so 0 is ok.
                if intData[i] != 0 and intData[i] != 1:
                    raise Exception
            elif not (0 < intData[i] <= checkList[i]):      # Taking advantage of python if statements.
                raise Exception

        cursor.execute("select id from events where code = "  # See if 'code' is for real event.
                       + str(code) + ' and "'
                       + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       + '" between startTime and endTime')
        if not cursor.fetchone():
            raise Exception

        return True
    except Exception:
        return False

def putInDatabase(s):
    cursor = safeCursor()
    data = s.split('/')                                     # Formatting the sql query.
    code = data.pop()
    values = '"' + data[0] + '"'
    for i in range(1,len(data)):
        values += ', ' + data[i]
                                                            # Replace event code with foreign key id.
    cursor.execute("select id from events where code = " + str(code) + ' and "'
                   + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                   + '" between startTime and endTime')
    eventID = cursor.fetchone()[0]

    values += ', ' + str(eventID)                           # This is the order of descriptors.
    sql = "INSERT INTO attendance (stuID, sex, race, age, major, minor, major2, minor2," \
          " gradYear, program, housing, transfer, latinx, lgbtq, event, access)" \
          " VALUES (" + values + ', "' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '");'

    cursor.execute(sql)
    mysql.connection.commit()

@app.route('/submit-attendance', methods=['GET', 'POST'])
def attend():
    if request.method == 'POST':
        s = request.form['s']
        if checkString(s):
            putInDatabase(s)
            return 'success'
    return 'failure'

def fillQR(y):
    x = {}
    for i in range(len(y)):
        if y[i][0] == "other":      # Set other as main/no edit option.
            x[0] = "other"
        elif y[i][0] == "None":     # Specific to majors.
            x[0] = "None"
        else:
            x[i+1] = y[i][0]
    return x

def replaceFillQR(s,l,term):
    if s == '0':
        spot = 0
        for i in l:
            spot += 1
            if term in i:          # Queries are set up weird -> (('male',),('female',),('other',)).
                break
        return str(spot)           # Simple swap with original value of generic option.
    return s

@app.route('/qr', methods=['GET', 'POST'])
def qr():
    global sexQuery,raceQuery,majorQuery

    if request.method == 'POST':
        r = [request.form["stuID"],   # Order r for qr data to match correctly.
             replaceFillQR(request.form["sex"], sexQuery, 'other'),
             replaceFillQR(request.form["race"], raceQuery, 'other'), request.form.get("age"),
             replaceFillQR(request.form["major1"], majorQuery, 'None'),
             replaceFillQR(request.form["minor1"], majorQuery, 'None'),
             replaceFillQR(request.form["major2"], majorQuery, 'None'),
             replaceFillQR(request.form["minor2"], majorQuery, 'None'), request.form.get("gradYear"),
             request.form.get("program"), request.form.get("housing"), request.form.get("transfer"),
             request.form.get("latinx"), request.form.get("lgbtq")]

        s = ''
        for val in r:                           # Make temp string.
            if val is None:
                val = 0
            if val == 'on':                     # Handling weird inputs from form.
                val = 1
            s += str(val) + "/"                 # # necessary for end of qr string. to be replaced
        s += "#"                                # by code from scanner.
        return render_template("qrDisplay.html", s=s)

    sexs = fillQR(sexQuery)
    races = fillQR(raceQuery)
    majors = fillQR(majorQuery)
    return render_template("qr.html", sexs=sexs, races=races, majors=majors)

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     return render_template("test.html")

@app.errorhandler(500)
def err401(err):
    return render_template('error.html', err=err, login=(not current_user.is_authenticated))

@app.errorhandler(404)
def err404(err):
    return render_template('error.html', err=err, login=(not current_user.is_authenticated))

@app.errorhandler(401)
def err401(err):
    return render_template('error.html', err=err, login=(not current_user.is_authenticated))

if __name__ == '__main__':
    app.run()
