import datetime
import flask_mysqldb

from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static/')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cs_495'

mysql = flask_mysqldb.MySQL(app)

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

        for instance in data:                           # should all be (able to be) ints
            if not instance.isnumeric():
                raise Exception                         # 'raise Exception' just kicks code to the 'return False'

        stuID = data.pop(0)                             # check format of studentID
        if len(stuID) != 6 or int(stuID) < 0:
            raise Exception

        intData = list(map(int,data))                   # for testing the value in the string
        code = intData.pop()

        if not checkList:                               # one-time set up of values to test against
            setUpCheckList()
        for i in range(len(checkList)):                 # check values against constraints
            if not (0 < intData[i] <= checkList[i]):    # Taking advantage of python if statements
                raise Exception

        cursor = mysql.connection.cursor()              # testing 'code' for getting an event
                                                        # (see if 'code' is for real event)

        cursor.execute("select id from events where code = " + str(code) + ' and "'
                               + str(datetime.datetime.now().replace(microsecond=0))
                               + '" between startTime and endTime')
        if not cursor.fetchone():
            raise Exception

        return True
    except Exception as e:
        print(e)
        return False

def putInDatabase(s):
    cursor = mysql.connection.cursor()

    data = s.split('/')                         # formatting the sql query
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

@app.route('/', methods=['GET', 'POST'])
def home():
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
    return render_template('error.html', err=err)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
