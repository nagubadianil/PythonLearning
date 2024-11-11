from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    position = db.Column(db.String(100), nullable=True)
    profile_image = db.Column(db.String(100), nullable=True)  # Stores filename of the image

    def __repr__(self):
        return f'<Employee {self.name}>'
