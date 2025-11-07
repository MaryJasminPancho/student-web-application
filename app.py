import sys
import os
sys.path.insert(0,"db/")
from db.dbhelper import  *
from werkzeug.utils import secure_filename

from flask import Flask, render_template, redirect, request, flash, url_for

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "mysecretkey"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index() -> None:
    students:list = getall('students')
    return render_template('index.html', studentlist=students, edit_students=None)

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
   
    image = request.files.get('profile_pic')
    filename = 'profile.png'

    if image and image.filename != "":
        filename = secure_filename(idno + "_" +  image.filename)
        image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path) 

    addrecord("students", idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=filename)
    flash("Student added successfully!")
    return redirect("/")

@app.route("/delete/<idno>")
def deletestudent(idno):
    student = getrecord("students", idno=idno)
    image = student[0]['image']

    deleterecord("students", idno=idno)

    if image and image != "profile.png":
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
        if os.path.exists(image_path):
            os.remove(image_path)

    flash("Student deleted successfully!")
    return redirect("/")

@app.route("/edit/<idno>")
def editstudent(idno):
    student = getrecord("students", idno=idno)
    if not student:
        return redirect("/")
    
    students = getall('students')
    return render_template("index.html", studentlist=students, edit_student=student[0])

@app.route("/update/<idno>", methods=["post"])
def updatestudent(idno):
    student = getrecord("students", idno=idno)[0]
    old_image = student["image"]

    lastname = request.form["lastname"].strip()
    firstname = request.form["firstname"].strip()
    course = request.form["course"]
    level = request.form["level"]

    file = request.files.get("profile_pic")

    if file and file.filename != "":
        new_filename = secure_filename(idno + "_" +file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))

        if old_image != "profile.png":
            old_path = os.path.join(app.config["UPLOAD_FOLDER"], old_image)
            if os.path.exists(old_path):
                os.remove(old_path)
    else:
        new_filename = old_image


    if not lastname or not firstname:
        flash("Fields cannot be empty!", "error")
        return redirect("/")
    
    # image = request.files.get('profile_pic')

    # if image and image.filename.strip() != "":
    #     filename = secure_filename(f"{idno}_{image.filename}")
    #     save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    #     image.save(save_path)

    updaterecord("students", where={"idno":idno}, lastname=lastname, firstname=firstname, course=course, level=level, image=new_filename)
    flash("Student updated successful", "success")
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)