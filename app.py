from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    course = db.Column(db.String(200), nullable = False)
    maths = db.Column(db.Integer, nullable = False)
    english = db.Column(db.Integer, nullable = False)
    hindi = db.Column(db.Integer, nullable = False)
    science = db.Column(db.Integer, nullable = False)

    profile = db.relationship("Profile", backref="student", uselist= False)

    def to_dict(self):
        return {
            "id": self.id,
            "name" : self.name,
            "course" : self.course,
            "math" : self.maths,
            "eng" : self.english,
            "hindi" : self.hindi,
            "science" : self.science
        }
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable= False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    def to_dict(self):
        return{
            "id" : self.id,
            "phone" : self.phone,
            "address" : self.address,
            "student_id" : self.student_id
         }
    
class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key = True )
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique=True)

    subjects = db.relationship("Subject", backref="teacher")

    def to_dict(self): 
        return {
        "id" : self.id,
        "name" : self.name,
        "email" : self.email
        }
    
class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer , primary_key = True)
    S_name = db.Column(db.String(100), nullable = False)
    teacher_id = db.Column(db.Integer,db.ForeignKey("teachers.id"), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "sub_name": self.S_name,
            "teacher_id": self.teacher_id
        }

@app.route("/api/students", methods = ["GET"])
def student():
    students = Student.query.all()

    return jsonify({
        "Total_students" : len(students),
        "students" : [s.to_dict() for s in students]
    })

@app.route("/api/students", methods = ["POST"])
def add_student():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid json data"}),400

        student = Student(
            name = data.get("name"),
            course = data.get("course"),
            maths = data.get("math"),
            english = data.get("eng"),
            hindi = data.get("hindi"),   
            science = data.get("science")
            )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message" : "Student added successfully"})
    except:
        return jsonify({"error":"Something went wrong"}),500


@app.route("/api/students/<int:id>", methods = ["PUT"])
def update_student(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error":"Invalid json data"}),400

        student = db.session.get(Student, id)

        if not student:
            return jsonify({"error":"The student is not found"}),404

        student.name = data.get("name", student.name)
        student.course = data.get("course", student.course)

        db.session.commit()

        return jsonify ({
            "message":"Student updated sucesfully",
            "student": student.to_dict()
            })
    except:
        return jsonify({"error":"Something went wrong"}),500
    

@app.route("/api/students/<int:id>", methods = ["DELETE"])
def delete_student(id):
    
    try:
        student = db.session.get(Student, id)

        if not student:
            return jsonify({"error":"Student not found"}),404
    
        db.session.delete(student)
        db.session.commit()

        return jsonify({
            "message":"student deleted successfully",
            "student":student.to_dict()
            })
    
    except:
        return jsonify({"error":"something went wrong"}),500
    

@app.route("/api/student-marks/<int:id>", methods= ["GET"])
def marks(id):

    student = db.session.get(Student, id)
    if not student:
        return jsonify({"error":"Student not found"}),404


    return jsonify({
        "id": student.id,
        "name": student.name,
        "course": student.course,
        "Maths": student.maths,
        "english": student.english,
        "hindi": student.hindi,
        "science": student.science,
    })


@app.route("/api/teachers", methods = ["POST"])
def add_teacher():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid json data"}),400

        teacher = Teacher(
            name = data.get("name"),
            email = data.get("email")
        )

        db.session.add(teacher)
        db.session.commit()

        return jsonify({
            "meassage": "teacher added successfully",
            "teacher": teacher.to_dict()
            })
    
    except:
        return jsonify({"error":"something went wrong"}),500

@app.route("/api/subjects", methods = ["POST"])
def add_subject():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid json data"}),400

        subject = Subject(
            S_name = data.get("sub_name"),
            teacher_id = data.get("teacher_id")
        )

        db.session.add(subject)
        db.session.commit()

        return jsonify({
            "message": "subject added successfully"
        })
    
    except:
        return jsonify({"error":"something went wrong"}),500


@app.route("/api/teacher/<int:id>", methods = ["GET"])
def get_teacher(id):
    data = db.session.get(Teacher, id)

    if not data:
        return jsonify({"error":"Teacher not found"}),404
    
    return jsonify({
        "id": data.id,
        "name": data.name,
        "email" : data.email,
        "subjects": [
            {
                "id": subject.id,
                "name": subject.S_name
            }
    for subject in data.subjects
        ]
    })

@app.route("/api/profile", methods = ["POST"])
def add_profile():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid json data"}),400
        
        profile = Profile(
            phone = data.get("phone"),
            address = data.get("address"),
            student_id = data.get("student_id")
        )

        db.session.add(profile)
        db.session.commit()

        return jsonify({"message":"Profile aaded successfully"})
    
    except:
        return jsonify({"error":"something went wrong"}),500
    
@app.route("/api/student/<int:id>/profile/" , methods = ["GET"])
def get_profile(id):
    try:
        data = db.session.get(Student, id)

        if not data:
            return jsonify({"error":"student not found not found"}),404
        
        return jsonify({
            "name": data.name,
            "id" : data.id,
            "profile" : 
                {
                    "phone" : data.profile.phone,
                    "address" : data.profile.address
                }
        })
    except:
        return jsonify({
            "error":"something went wrong"
        }),500
    
@app.route("/test", methods = ["GET"])
def test():
    return "api is ok"


if __name__=="__main__":
    app.run(debug=True)
