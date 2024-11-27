import requests
import json

BASE_URL = 'https://q8qmdclj-5001.use.devtunnels.ms'  # Change to your API base URL if different

# Create an employee
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
        print(f"Failed to create employee")

# Get the list of employees
def get_employees():
    url = f"{BASE_URL}/employees"
    response = requests.get(url)
    if response.status_code == 200:
        employees = response.json()
        print(f"Employees: {json.dumps(employees, indent=2)}")
    else:
        print("Failed to get employees")

# Get an employee by ID
def get_employee_by_id(employee_id):
    url = f"{BASE_URL}/employee/{employee_id}"
    response = requests.get(url)
    if response.status_code == 200:
        employee = response.json()
        print(f"Employee: {json.dumps(employee, indent=2)}")
    else:
        print(f"Failed to get employee with ID {employee_id}")

# Update an employee
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
        print(f"Failed to update employee with ID {employee_id}")

# Delete an employee
def delete_employee(employee_id):
    url = f"{BASE_URL}/employee/{employee_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Employee with ID {employee_id} deleted")
    else:
        print(f"Failed to delete employee with ID {employee_id}")

# Upload profile image for an employee
def upload_profile_image(employee_id, image_path):
    url = f"{BASE_URL}/employee/{employee_id}/upload"
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print(f"Profile image uploaded for employee with ID {employee_id}")
        else:
            print(f"Failed to upload image")

# Download the CSV of employees
def download_employees_csv():
    url = f"{BASE_URL}/employee/download/csv"
    response = requests.get(url)
    if response.status_code == 200:
        with open('employees.csv', 'wb') as f:
            f.write(response.content)
        print("CSV file of employees downloaded as 'employees.csv'")
    else:
        print(f"Failed to download CSV")

# Main function to perform all operations
def main():
    # 1. Create Employees
    create_employee("Anil Nagubadi", "nagubadianil@example.com", "Software Developer")
    create_employee("Amulya Thota", "amulya75@gmail.com", "School Co-ordinater")
    
    # 2. Get All Employees
    get_employees()
    
    # 3. Get Employee by ID
    get_employee_by_id(1)  # Assuming employee with ID 1 exists

    # 4. Update Employee
    update_employee(1, "Alice Smith", "alice.smith.updated@example.com", "Manager")
    
    # 5. Delete Employee
    delete_employee(2)  # Assuming employee with ID 2 exists

    # 6. Upload Profile Image for an Employee
    # Note: Change the path to an actual image file you want to upload
    #upload_profile_image(1, 'path_to_image.jpg')

    # 7. Download Employees CSV
    download_employees_csv()

if __name__ == "__main__":
    main()
