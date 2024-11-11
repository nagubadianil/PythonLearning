from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import csv
from models import db, Employee
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Setup image upload folder
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/employees', methods=['GET'])
def get_employees():
    """Get the list of all employees."""
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'email': emp.email, 'position': emp.position} for emp in employees])


@app.route('/employee', methods=['POST'])
def create_employee():
    """Create a new employee."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    position = data.get('position')

    if not name or not email:
        return jsonify({"message": "Name and email are required!"}), 400

    # Create a new Employee record
    new_employee = Employee(name=name, email=email, position=position)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee created!"}), 201


@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    """Get a single employee by ID."""
    employee = Employee.query.get_or_404(id)
    return jsonify({'id': employee.id, 'name': employee.name, 'email': employee.email, 'position': employee.position})


@app.route('/employee/<int:id>', methods=['PUT'])
def update_employee(id):
    """Update an employee by ID."""
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    employee.name = data.get('name', employee.name)
    employee.email = data.get('email', employee.email)
    employee.position = data.get('position', employee.position)
    
    db.session.commit()
    return jsonify({"message": "Employee updated!"})


@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """Delete an employee by ID."""
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted!"})


@app.route('/employee/<int:id>/upload', methods=['POST'])
def upload_profile_image(id):
    # """Upload profile image for an employee."""
    # employee = Employee.query.get_or_404(id)
    # if 'file' not in request.files:
    #     return jsonify({"message": "No file part!"}), 400

    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({"message": "No selected file!"}), 400

    # if file and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
    #     filename = photos.save(file, name=f"{id}_")
    #     employee.profile_image = filename
    #     db.session.commit()
    #     return jsonify({"message": "Profile image uploaded!"})

    return jsonify({"message": "File not allowed!"}), 400


@app.route('/employee/download/csv', methods=['GET'])
def download_csv():
    """Download a CSV file with employee data."""
    employees = Employee.query.all()
    filename = 'employees.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Email', 'Position'])
        for employee in employees:
            writer.writerow([employee.id, employee.name, employee.email, employee.position])

    return send_from_directory(directory=os.getcwd(), path=filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
