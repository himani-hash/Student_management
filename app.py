from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = "Students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    course = db.Column(db.String(200), nullable = False)

    def to_dict(self):
        return{
            "id": self.id,
            "name" : self.name,
            "course" : self.course
        }

with app.app_context():
    db.create_all()



@app.route("/student", methods = ["GET"])
def student():
    students = Student.query.all()

    return jsonify({
        "Total_students" : len(students),
        "students" : [s.to_dict() for s in students]
    })

@app.route("/add-student", methods = ["POST"])
def add_student():
    data = request.get_json()

    student = Student(
       name = data.get("name"),
       course = data.get("course")
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message" : "Student added sucessfully"
    })

@app.route("/update-student/<int:id>", methods = ["POST"])
def update_student(id):
    data = request.get_json()

    student = Student.query.get(id)

    if not student:
        return jsonify({"error":"The student is not found"}),404

    student.name = data.get("name", student.name)
    student.course = data.get("course", student.course)

    db.session.commit()

    return({
        "message":"Student updated succesfully",
        "student": student.to_dict()
        })

@app.route("/delete-student/<int:id>", methods = ["DELETE"])
def delete_student(id):
    
    student = Student.query.get(id)

    if not student:
        return{"error":"Student not found"},404
    
    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message":"student dleetd successfully",
        "student":student.to_dict()
    })

if __name__=="__main__":
    app.run(debug=True)