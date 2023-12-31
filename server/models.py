from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)

    # Add relationship
    
    # Add serialization

    # Add validation

    
    
    def __repr__(self):
        return f'<Student {self.id}>'

class Subject(db.Model, SerializerMixin):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # Add relationship
    
    # Add serialization
    
    def __repr__(self):
        return f'<Subject {self.id}>'

class SubjectEnrollment(db.Model, SerializerMixin):
    __tablename__ = 'subject_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    enrollment_year = db.Column(db.Integer, nullable=False)

    # Add relationships
    
    # Add serialization
    
    # Add validation
    
    def __repr__(self):
        return f'<SubjectEnrollment {self.id}>'


