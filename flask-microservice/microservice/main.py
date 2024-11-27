from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

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

@app.route('/', methods=['GET'])
def get_readme():
    text = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rushi's Sample Employee Rest Service</title>
</head>
<body>
    <h1>Rushi's Sample Employee Rest Service</h1>

  <h2>Imports and Initializing </h2>
    <pre><code class="language-python">
import requests
import json

BASE_URL = 'https://q8qmdclj-5001.use.devtunnels.ms'  # Change to your API base URL if different

    </code></pre>
    
    <h2>Create an employee</h2>
    <pre><code class="language-pyhton">
def create_employee(name, email, position):
    url = f"{BASE_URL}/employee"
    data = {
        "name": name,
        "email": email,
        "position": position
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print(f"Employee created: {name}")
    else:
        print(f"Failed to create employee: {response.json()}")
    </code></pre>

    <h2>Get the list of employees</h2>
    <pre><code class="language-python">
def get_employees():
    url = f"{BASE_URL}/employees"
    response = requests.get(url)
    if response.status_code == 200:
        employees = response.json()
        print(f"Employees: {json.dumps(employees, indent=2)}")
    else:
        print("Failed to get employees")

    </code></pre>
        <h2>Get an employee by ID</h2>
    <pre><code class="language-python">
def get_employee_by_id(employee_id):
    url = f"{BASE_URL}/employee/{employee_id}"
    response = requests.get(url)
    if response.status_code == 200:
        employee = response.json()
        print(f"Employee: {json.dumps(employee, indent=2)}")
    else:
        print(f"Failed to get employee with ID {employee_id}: {response.json()}")

    </code></pre>
        <h2>Update an employee</h2>
    <pre><code class="language-python">
def update_employee(employee_id, name, email, position):
    url = f"{BASE_URL}/employee/{employee_id}"
    data = {
        "name": name,
        "email": email,
        "position": position
    }
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print(f"Employee with ID {employee_id} updated")
    else:
        print(f"Failed to update employee with ID {employee_id}: {response.json()}")

    </code></pre>
        <h2>Delete an employee</h2>
    <pre><code class="language-python">
def delete_employee(employee_id):
    url = f"{BASE_URL}/employee/{employee_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Employee with ID {employee_id} deleted")
    else:
        print(f"Failed to delete employee with ID {employee_id}: {response.json()}")

    </code></pre>
        <h2>Download the CSV of employees</h2>
    <pre><code class="language-python">
def download_employees_csv():
    url = f"{BASE_URL}/employee/download/csv"
    response = requests.get(url)
    if response.status_code == 200:
        with open('employees.csv', 'wb') as f:
            f.write(response.content)
        print("CSV file of employees downloaded as 'employees.csv'")
    else:
        print(f"Failed to download CSV: {response.json()}")
    </code></pre>
        <h2>Main function to perform all operations</h2>
    <pre><code class="language-python">
def main():
    # 1. Create Employees
    create_employee("Alice Smith", "alice.smith@example.com", "Software Developer")
    create_employee("Bob Johnson", "bob.johnson@example.com", "Product Manager")
    
    # 2. Get All Employees
    get_employees()
    
    # 3. Get Employee by ID
    get_employee_by_id(1)  # Assuming employee with ID 1 exists

    # 4. Update Employee
    update_employee(1, "Alice Smith Updated", "alice.smith.updated@example.com", "Senior Software Developer")
    
    # 5. Delete Employee
    delete_employee(2)  # Assuming employee with ID 2 exists

    # 6. Upload Profile Image for an Employee
    # Note: Change the path to an actual image file you want to upload
    #upload_profile_image(1, 'path_to_image.jpg')

    # 7. Download Employees CSV
    download_employees_csv()
    </code></pre>
        <h2>main guard</h2>
    <pre><code class="language-python">
    if __name__ == "__main__":
        main()
    </code></pre>
</body>
</html>
    """

    return text


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
    app.run(debug=True, host="0.0.0.0", port=5001)
