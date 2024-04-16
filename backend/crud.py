from sqlalchemy.orm import Session
from model import Employee, EmployeeType
from schemas import EmployeeBase, EmployeeTypeBase
from datetime import date
from typing import Optional

#get all employee data
def get_employee(db:Session,skip:int=0,limit:int=100):
    return db.query(Employee).offset(skip).limit(limit).all()

#get all employee type 
def get_employee_type(db:Session):
    return db.query(EmployeeType).all()

#get employee by id
def get_employee_by_id(db:Session,employee_id:int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

#get employee by name
def get_employee_by_name(db:Session,first_name:str,last_name:str,email:str):
    return db.query(Employee).filter(Employee.first_name == first_name,Employee.last_name == last_name,Employee.email == email).first()

#create employee
def create_employee(db:Session, employee: EmployeeBase):
    _employee = Employee(
                        first_name=employee["first_name"],
                        last_name=employee["last_name"],
                        email=employee["email"],
                        employee_type=employee["employee_type"],
                        benefits=employee["benefits"],
                        leaves=employee["leaves"],
                        project=employee["project"],
                        contract_end=employee["contract_end"],
                        )
    employees = []
    db.add(_employee)
    db.commit()
    db.refresh(_employee)
    employees.append(_employee)
    return employees

#get employee type by desscription
def get_employee_type_by_desc(db:Session,description:str):
    return db.query(EmployeeType).filter(EmployeeType.description == description).first()

#get employee type by id
def get_employee_type_by_id(db:Session,id:id):
    return db.query(EmployeeType).filter(EmployeeType.id == id).first()

#create employee type
def create_employee_type(db:Session, employee_type: EmployeeTypeBase):
    _employee_type = EmployeeType(
                        description=employee_type.description
                        )
    db.add(_employee_type)
    db.commit()
    db.refresh(_employee_type)
    return _employee_type

#delete employee
def remove_employee(db:Session,employee_id:int):
    _employee = get_employee_by_id(db=db,employee_id=employee_id)
    db.delete(_employee)
    db.commit()

#update employee
def update_employee(db:Session,
                employee_id:int,
                first_name:str,
                last_name:str,
                email:str,
                employee_type:int,
                benefits:Optional[str],
                leaves:Optional[int],
                project:Optional[str],
                contract_end:Optional[date]
                ):
    _employee = get_employee_by_id(db=db,employee_id=employee_id)
    _employee.first_name = first_name
    _employee.last_name = last_name
    _employee.email = email
    _employee.employee_type = employee_type
    _employee.benefits = benefits
    _employee.leaves = leaves
    _employee.project = project
    _employee.contract_end = contract_end
    db.commit()
    db.refresh(_employee)
    return _employee
