from flask import Blueprint, jsonify, request
from models import db, Student, Course, Profile, Teacher, Subject

api = Blueprint('api',__name__)

@api.route("/api/students", methods = ["GET"])
def student():
    students = Student.query.all()

    return jsonify({
        "Total_students" : len(students),
        "students" : [s.to_dict() for s in students]
    })

@api.route("/api/courses", methods = ["POST"])
def add_course():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid json data"}),400
        
        course = Course(
            course = data.get("course")
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({
            "message": "Course added successfully",
            "course": course.to_dict()
            }), 201

    except:
        return jsonify({"error":"something went wrong"})
    
@api.route("/api/enroll", methods=["POST"])
def enroll_student():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        student_id = data.get("student_id")
        course_id = data.get("course_id")

        if not student_id or not course_id:
            return jsonify({"error": "student_id and course_id required"}), 400

        student = db.session.get(Student, student_id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        course = db.session.get(Course, course_id)
        if not course:
            return jsonify({"error": "Course not found"}), 404

        if course in student.courses:
            return jsonify({"message": "Student already enrolled in this course"}), 400

        student.courses.append(course)

        db.session.commit()

        return jsonify({
            "message": "Student enrolled successfully",
            "student_id": student.id,
            "course_id": course.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@api.route("/api/unenroll", methods=["POST"])
def unenroll_student():
    data = request.get_json()

    student = db.session.get(Student, data.get("student_id"))
    course = db.session.get(Course, data.get("course_id"))

    if not student or not course:
        return jsonify({"error": "Invalid student or course"}), 404

    if course not in student.courses:
        return jsonify({"error": "Student not enrolled in this course"}), 400

    student.courses.remove(course)
    db.session.commit()

    return jsonify({"message": "Unenrolled successfully"})


@api.route("/api/student/<int:id>/courses", methods = ["GET"])
def get_student_courses(id):
    try:
        student = db.session.get(Student, id)

        if not student:
            return jsonify({"error": "Student not found"}), 404

        courses_list = []

        for course in student.courses:
            courses_list.append({
                "id": course.id,
                "name": course.name
            })

        return jsonify({
            "student_id": student.id,
            "student_name": student.name,
            "enrolled_courses": courses_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route("/api/courses/<int:id>/students", methods = ["GET"])
def get_course_students(id):
    try:
        course = db.session.get(Course, id)

        if not course:
            return jsonify({"error": "Course not found"}), 404

        students_list = []

        for student in course.students:
            students_list.append({
                "id": student.id,
                "name": student.name
            })

        return jsonify({
            "course_id": course.id,
            "course_name": course.name,
            "enrolled_students": students_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/api/students", methods = ["POST"])
def add_student():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid json data"}),400

            
        student = Student(
            name=data.get("name"),
            maths=data.get("math"),
            english=data.get("eng"),
            hindi=data.get("hindi"),
            science=data.get("science"),
            course_id=data.get("course_id")
            )


        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message" : "Student added successfully"})
    except:
        return jsonify({"error":"Something went wrong"}),500


@api.route("/api/students/<int:id>", methods = ["PUT"])
def update_student(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error":"Invalid json data"}),400

        student = db.session.get(Student, id)

        if not student:
            return jsonify({"error":"The student is not found"}),404

        student.name = data.get("name", student.name)
        student.course_id = data.get("course_id", student.course_id)

        db.session.commit()

        return jsonify ({
            "message":"Student updated sucesfully",
            "student": student.to_dict()
            })
    except:
        return jsonify({"error":"Something went wrong"}),500
    

@api.route("/api/students/<int:id>", methods = ["DELETE"])
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
    

@api.route("/api/student-marks/<int:id>", methods= ["GET"])
def marks(id):

    student = db.session.get(Student, id)
    if not student:
        return jsonify({"error":"Student not found"}),404


    return jsonify({
        "id": student.id,
        "name": student.name,
        "Maths": student.maths,
        "english": student.english,
        "hindi": student.hindi,
        "science": student.science,
    })


@api.route("/api/teachers", methods = ["POST"])
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

@api.route("/api/subjects", methods = ["POST"])
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


@api.route("/api/teacher/<int:id>", methods = ["GET"])
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

@api.route("/api/profiles", methods = ["POST"])
def add_profile():
    try:
        data = request.get_json()

        student = db.session.get(Student, data.get("student_id"))


        if not data:
            return jsonify({"error":"Invalid json data"}),400
        
        if student.profile:
            return jsonify({"error": "Profile already exists for this student"}), 400
        
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
    
@api.route("/api/student/<int:id>/profile" , methods = ["GET"])
def get_profile(id):
    try:
        data = db.session.get(Student, id)

        if not data:
            return jsonify({"error":"student not found not found"}),404
        
        if not data.profile :
            return jsonify({"error":"profile not found"},404)

        
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
    
@api.route("/test", methods = ["GET"])
def test():
    return "api is ok"
