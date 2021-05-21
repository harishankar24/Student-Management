from flask import Flask, render_template, redirect, url_for, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
  roll_no = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(50), nullable = False)
  marks_in_maths = db.Column(db.Integer, nullable = False)
  marks_in_physics = db.Column(db.Integer, nullable = False)
  marks_in_chemistry = db.Column(db.Integer, nullable = False)
  total_marks = db.Column(db.Integer, nullable = False)
  marks_percentage = db.Column(db.Float, nullable = False)
  rank = db.Column(db.Integer, nullable = False)


@app.route("/")
def home():
  all_students_data = Student.query.order_by(Student.roll_no).all()
  return render_template('index.html', students = all_students_data)


@app.route("/sorted")
def sorted():
  all_students_data = Student.query.order_by(Student.total_marks.desc()).all()
  for i in range(len(all_students_data)):
    all_students_data[i].rank = i+1  
  db.session.commit()
  return render_template('rank.html', students = all_students_data)


@app.route("/search", methods = ['GET','POST'])
def search():
  name = request.form['name']
  search_results = Student.query.filter_by(name = name.title())
  return render_template('index.html', students = search_results)


@app.route("/insert", methods = ['POST'])
def insert():
  roll = int(request.form['roll'])
  name = request.form['name']
  math = int(request.form['marks_in_maths'])
  physics = int(request.form['marks_in_physics'])
  chemistry = int(request.form['marks_in_chemistry'])
  total = math + physics + chemistry
  new_record = Student(
    roll_no = roll,
    name = name.title(),
    marks_in_maths = math,
    marks_in_physics = physics,
    marks_in_chemistry = chemistry,
    total_marks = total,
    marks_percentage = round(total/3,1),
    rank = 0
  )
  db.session.add(new_record)
  db.session.commit()
  flash('Student added successfully')
  print(roll,name,math,physics,chemistry,total)
  return redirect(url_for('home'))


@app.route('/delete/<id>', methods = ['GET','POST'])
def delete(id):
  student = Student.query.get(id)
  db.session.delete(student)
  db.session.commit()
  flash("Student deleted successfully")
  return redirect(url_for('home'))


@app.route('/update/<id>', methods = ['GET', 'POST'])
def update(id):
  if request.method == 'POST':
    student = Student.query.get(id)
    name = request.form['name']
    math = int(request.form['marks_in_maths'])
    physics = int(request.form['marks_in_physics'])
    chemistry = int(request.form['marks_in_chemistry'])
    total = math + physics + chemistry
    student.name = name.title()
    student.marks_in_maths = math
    student.marks_in_physics = physics
    student.marks_in_chemistry = chemistry
    student.total_marks = total
    student.marks_percentage = round(total/3,1)
    db.session.commit()
    flash("Student details updated successfully")
    return redirect(url_for('home'))
  
if __name__ == "__main__":
  app.run(debug=True, port=8000)