import sys
sys.path.insert(0,"db/")
from db.dbhelper import  *

from flask import Flask, render_template, redirect, request, flash

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route("/")
def index() -> None:
    students:list = getall('students')
    return render_template('index.html', studentlist=students)

@app.route("/add", methods=["post"])
def addstudent() -> None:
    idno = request.form['idno'].strip()
    lastname = request.form['lastname'].strip()
    firstname = request.form['firstname'].strip()
    course = request.form['course']
    level = request.form['level']

    if not idno or not lastname or not firstname:
        flash("Please fill in all required fields!", "error")
        return redirect("/")

    addrecord("students", idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
    flash("Student added successfully!")
    return redirect("/")

@app.route("/delete/<idno>")
def deletestudent(idno):
    deleterecord("students", idno=idno)
    return redirect("/")

@app.route("/edit/<idno>", methods=["get"])
def editstudent(idno):
    student = getrecord("students", idno=idno)
    if not student:
        return redirect("/")
    return render_template("edit.html", student=student[0])

@app.route("/update", methods=["post"])
def updatestudent() -> None:
    idno = request.form["idno"]
    lastname = request.form["lastname"]
    firstname = request.form["firstname"]
    course = request.form["course"]
    level = request.form["level"]

    # sql = "UPDATE students SET lastname=?, firstname=?, course=?, level=? WHERE idno=?"
    # vals = [lastname, firstname, course, level, idno]
    # getprocess(sql, vals)
    # return redirect("/")
    updaterecord("students", where={"idno":idno}, lastname=lastname, firstname=firstname, course=course, level=level)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)