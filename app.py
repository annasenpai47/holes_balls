from flask import Flask, render_template, request, flash
from flask_pymysql import MySQL

MAX_AM = 10000

app = Flask(__name__)

pymysql_connect_kwargs = {'host': '127.0.0.1',
                          'port' : 3306,
                          'user': 'root',
                          'password': '',
                          'database': 'balls_holes'}

app.config['pymysql_kwargs'] = pymysql_connect_kwargs
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'
mysql = MySQL(app)

def find_Max():
    cursor = mysql.connection.cursor()
    select = 'SELECT * FROM `hoba` WHERE ball = (SELECT MAX(ball) FROM `hoba`) ORDER BY hole '
    cursor.execute(select)
    select = cursor.fetchall()
    a = str(select[0][1])
    b = str(select[0][2])
    flash("В " + a + " ячейке" + " " + b + " шариков")

def checkBalls(h):
    cursor = mysql.connection.cursor()
    select = 'SELECT ball FROM `hoba` WHERE hole = (%s)'
    cursor.execute(select, h)
    select = cursor.fetchall()
    am = select[0][0]
    if am > MAX_AM:
        am = am % MAX_AM
        if am == 0:
            am = MAX_AM
        update = 'UPDATE `hoba` SET `ball`= (%s) WHERE `hole` = (%s)'
        cursor.execute(update, (am, h))
        mysql.connection.commit()


def isUnic(h):
    cursor = mysql.connection.cursor()
    select = 'SELECT ball FROM `hoba` WHERE hole = (%s)'
    cursor.execute(select, h)
    select = cursor.fetchall()
    if len(select) == 0:
        return -1
    else:
        return select[0][0]

def addBall(h,b):
    if h.isdigit() and b.isdigit() and int(h)>0:
        if isUnic(h)==-1:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO hoba (hole, ball) VALUES (%s,%s);", (h, b))
            mysql.connection.commit()
            checkBalls(h)
        else:
            cursor = mysql.connection.cursor()
            select = 'SELECT ball FROM `hoba` WHERE hole = (%s)'
            cursor.execute(select, h)
            select = cursor.fetchall()
            am = int(select[0][0])
            am += int(b)
            update = 'UPDATE `hoba` SET `ball`= (%s) WHERE `hole` = (%s)'
            cursor.execute(update, (am, h))
            mysql.connection.commit()
            checkBalls(h)

        flash('Шарики добавлены успешно!')
    else:
        flash('Данные некорректные!')


@app.route('/', methods =["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get('find_max') == "Найти максимальную ячейку":
            find_Max()
        else:
            h = request.form.get("index")
            b = request.form.get("amount")
            addBall(h, b)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

