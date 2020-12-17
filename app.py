from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Employee Class/Model
class Employee(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(40))
  lastname = db.Column(db.String(40))
  salary = db.Column(db.Float)
  hiredate = db.Column(db.String(200))
  position = db.Column(db.String(200))
  manager = db.Column(db.String(100))

  def __init__(self, firstname, lastname, salary, hiredate, position, manager):
    self.firstname = firstname
    self.lastname = lastname
    self.salary = salary
    self.hiredate = hiredate
    self.position = position
    self.manager = manager

# Employee Schema
class EmployeeSchema(ma.Schema):
  class Meta:
    fields = ('firstname', 'lastname', 'salary', 'hiredate', 'position', 'manager')

# Init schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Create a Employee
@app.route('/employee', methods=['POST'])
def add_employee():
  firstname = request.json['firstname']
  lastname = request.json['lastname']
  salary = request.json['salary']
  hiredate = request.json['hiredate']
  position = request.json['position']
  manager = request.json['manager']

  new_employee = Employee(firstname, lastname, salary, hiredate, position, manager)

  db.session.add(new_employee)
  db.session.commit()

  return employee_schema.jsonify(new_employee)

# Get All Employees
@app.route('/employees', methods=['GET'])
def get_employees():
  all_employees = Employee.query.all()
  result = employees_schema.dump(all_employees)
  return jsonify(result)

# Get Single Employees
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
  employee = Employee.query.get(id)
  return employee_schema.jsonify(employee)

# Update a Product
@app.route('/employee/<id>', methods=['PATCH'])
def update_employee(id):
  employee = Employee.query.get(id)

  firstname = request.json['firstname']
  lastname = request.json['lastname']
  salary = request.json['salary']
  hiredate = request.json['hiredate']
  position = request.json['position']
  manager = request.json['manager']


  employee.firstname = firstname
  employee.lastname = lastname
  employee.salary = salary
  employee.hiredate = hiredate
  employee.position = position
  employee.manager = manager

  db.session.commit()
  return employee_schema.jsonify(employee)

# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
  employee = Employee.query.get(id)
  db.session.delete(employee)
  db.session.commit()

  return employee_schema.jsonify(employee)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)