from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
DB_NAME = "college_companion.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS timetable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        subject TEXT,
                        time TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS assignments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        deadline TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/timetable", methods=["GET", "POST"])
def timetable():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        subject = request.form.get("subject")
        time = request.form.get("time")
        if subject and time:
            cursor.execute("INSERT INTO timetable (subject, time) VALUES (?, ?)", (subject, time))
            conn.commit()
        return redirect(url_for("timetable"))

    cursor.execute("SELECT subject, time FROM timetable")
    classes = cursor.fetchall()
    conn.close()
    return render_template("timetable.html", classes=classes)

@app.route("/assignments", methods=["GET", "POST"])
def assignments():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        deadline = request.form.get("deadline")
        try:
            datetime.strptime(deadline, "%Y-%m-%d")  # Validate date format
            cursor.execute("INSERT INTO assignments (name, deadline) VALUES (?, ?)", (name, deadline))
            conn.commit()
        except ValueError:
            pass  # Handle invalid date format
        return redirect(url_for("assignments"))

    cursor.execute("SELECT name, deadline FROM assignments")
    assignments_list = cursor.fetchall()
    conn.close()
    return render_template("assignments.html", assignments=assignments_list)

@app.route("/gpa", methods=["GET", "POST"])
def gpa():
    if request.method == "POST":
        grades = request.form.get("grades").split(",")
        try:
            grades = [float(g) for g in grades]
            gpa = sum(grades) / len(grades)
            return render_template("gpa.html", gpa=gpa)
        except ValueError:
            pass  # Handle invalid input
    return render_template("gpa.html", gpa=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
