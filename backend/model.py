from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from config import Base

class Employee(Base):
    __tablename__= 'employee'

    id=Column(Integer, primary_key=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String)
    employee_type=Column(Integer, ForeignKey("employee_type.id"))
    benefits=Column(String)
    leaves=Column(Integer)
    project=Column(String)
    contract_end=Column(Date)

class EmployeeType(Base):
    __tablename__= 'employee_type'

    id=Column(Integer, primary_key=True)
    description=Column(String)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String,nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    class Config():
        orm_mode = True



