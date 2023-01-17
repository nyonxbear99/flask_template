from flask import Flask, jsonify, request  # importing the necessary modules from flask
from flask_cors import CORS  # importing the cors module
from flask_sqlalchemy import SQLAlchemy  # importing the SQLAlchemy module



app = Flask(__name__) # creating a Flask application
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Library.sqlite3" # configuring the database URI
app.config["SECRET_KEY"] = "hello"
CORS(app) # enabling CORS
db = SQLAlchemy(app)  # initializing the database


class Student(db.Model):  # defining the Student model
    id = db.Column(db.Integer, primary_key=True)  # the primary key column
    name = db.Column(
        db.String(80), unique=True, nullable=False
    )  # name column with a max length of 80, unique and not nullable
    age = db.Column(
        db.Integer, unique=True, nullable=False
    )  # age column with a max length of 120, unique and not nullable

    def __init__(self,name,age):
        self.name = name
        self.age = age

@app.route("/student", methods=["POST"])  # route for creating a student
def create_student():
    data = request.get_json()  # retrieving the data from the request
    new_student = Student(
        name=data["name"], age=data["age"]
    )  # creating a new student object
    db.session.add(new_student)  # adding the student to the session
    db.session.commit()  # committing the changes to the database
    return jsonify(
        {"message": "Student created!"}
    )  # returning a message to confirm the creation


@app.route("/student/<student_id>", methods=["GET"])  # route for reading a student
def read_student(student_id):
    student = Student.query.get(student_id)  # retrieving the student from the database
    if student:  # if the student exists
        return jsonify(
            {"student": student.name, "age": student.age}
        )  # return the student's name and age
    else:
        return jsonify(
            {"message": "Student not found"}
        )  # return a message if the student is not found


@app.route("/student/<student_id>", methods=["PUT"])  # route for updating a student
def update_student(student_id):
    data = request.get_json()  # retrieving the data from the request
    student = Student.query.get(student_id)  # retrieving the student from the database
    if student:  # if the student exists
        student.name = data["name"]  # update the name
        student.age = data["age"]  # update the age
        db.session.commit()  # commit the changes to the database
        return jsonify(
            {"message": "Student updated!"}
        )  # return a message to confirm the update
    else:
        return jsonify(
            {"message": "Student not found"}
        )  # return a message if the student is not found


@app.route("/student/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted!"})
    else:
        return jsonify({"message": "Student not found"})


if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug = True)