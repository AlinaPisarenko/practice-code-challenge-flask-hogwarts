#!/usr/bin/env python3
from models import db, Student, Subject, SubjectEnrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api=Api(app)

class Students(Resource):
    def get(self):
        students = Student.query.all()
        response_body = [student.to_dict(rules=('-subject_enrollments',)) for student in students]

        return make_response(jsonify(response_body), 200)

api.add_resource(Students, '/students')


class StudentsById(Resource):
    def get(self, id):
        student = Student.query.filter(Student.id == id).first()

        if not student:
            response_body = {'error': 'Student not found'}
            return make_response(jsonify(response_body), 404)

        return make_response(jsonify(student.to_dict()), 200)

api.add_resource(StudentsById, '/students/<int:id>')


class Subjects(Resource):
    def get(self):
        subjects = Subject.query.all()
        response_body = [subject.to_dict(rules=('-subject_enrollments',)) for subject in subjects]

        return make_response(jsonify(response_body), 200)

api.add_resource(Subjects, '/subjects')

class SubjectsById(Resource):
    def get(self, id):
        subject = Subject.query.get(id)

        if not subject:
            response_body = {'error': 'Subject not found'}
            return make_response(jsonify(response_body), 404)

        return make_response(jsonify(subject.to_dict()), 200)

api.add_resource(SubjectsById, '/subjects/<int:id>')

class SubjectEnrollments(Resource):
    def post(self):
        try:
            json_data=request.get_json()

            new_enrollment = SubjectEnrollment(
                enrollment_year=json_data.get('enrollment_year'),
                student_id=json_data.get('student_id'),
                subject_id=json_data.get('subject_id')
                )
            
            db.session.add(new_enrollment)
            db.session.commit()

            response_body = new_enrollment.to_dict()

            return make_response(jsonify(response_body), 200)

        except ValueError:
            response_body = { "errors": ["validation errors"] }

            return make_response(jsonify(response_body), 400)


api.add_resource(SubjectEnrollments, '/subject_enrollments')

class SubjectEnrollmentsById(Resource):
    def delete(self, id):

        subject_enrollment  = SubjectEnrollment.query.get(id)

        if not subject_enrollment:
            response_body = {'error': 'Subject Enrollment not found'}
            return make_response(jsonify(response_body), 404)

        db.session.delete(subject_enrollment)
        db.session.commit()

        return make_response({}, 204)
    
            

api.add_resource(SubjectEnrollmentsById, '/subject_enrollments/<int:id>')

@app.route('/')
def home():
    return '<h1>🔮 Hogwarts Classes</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)
