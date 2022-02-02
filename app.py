import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static/')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        connection = sqlite3.connect("attendance.db")
        cursor = connection.cursor()
        s = request.form['s']
        data = s.split('/')
        values = ""
        for i in range(len(data)-1):
            values += '"' + data[i] + '"' + ', '
        values += '"' + data[-1] + '"'
        sql = "INSERT INTO attendance (stuID, sex, race, age, major, gradYear, event, planner)" \
              " VALUES (" + values + ");"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        return 'success'
    return 'failure'

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("index.html")

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

if __name__ == '__main__':
    app.run()
