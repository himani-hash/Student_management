from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import bcrypt

db = SQLAlchemy()

student_courses = db.Table(
    "student_courses",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True)
)

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    maths = db.Column(db.Integer, nullable=False)
    english = db.Column(db.Integer, nullable=False)
    hindi = db.Column(db.Integer, nullable=False)
    science = db.Column(db.Integer, nullable=False)

    courses = db.relationship("Course",secondary = student_courses,  backref="students")
    profile = db.relationship("Profile", backref="student", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "math": self.maths,
            "eng": self.english,
            "hindi": self.hindi,
            "science": self.science,
        }


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "course": self.course
        }


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "address": self.address,
            "student_id": self.student_id
        }


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)

    subjects = db.relationship("Subject", backref="teacher")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    S_name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "sub_name": self.S_name,
            "teacher_id": self.teacher_id
        }

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    is_verified = db.Column(db.Boolean, default = False)
    verification_token = db.Column(db.String(255), nullable = True)
    reset_token = db.Column(db.String(255), nullable = True)
    reset_token_expiry = db.Column(db.DateTime, nullable = True)
    created_at = db.Column(db.DateTime, default = lambda:datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))


    # def set_password(self, password):
    #     hashed = bcrypt.hashpw

