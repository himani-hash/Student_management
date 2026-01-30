from flask import Flask, jsonify, request

app = Flask(__name__)

students = []

@app.route("/student", methods = ["GET"])
def student():
    return jsonify({
        "Total_students" : len(students),
        "students" : students
    })

@app.route("/add student", methods = ["POST"])
def add_student():
    data = request.json

    student = {
        "id" : len(students)+1,
        "Name" : data.get("name"),
        "course" : data.get("course")
    }

    students.append(student)

    return jsonify({
        "message" : "Student added sucessfully"
    })

if __name__=="__main__":
    app.run(debug=True)