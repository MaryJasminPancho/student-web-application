import sys
sys.path.insert(0,"db/")
from db.dbhelper import  *

from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def index() -> None:
    students:list = getall('students')
    return render_template('index.html', studentlist=students)

if __name__=="__main__":
    app.run(debug=True)