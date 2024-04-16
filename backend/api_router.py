from fastapi import APIRouter, HTTPException, Path, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import EmployeeBase, EmployeeTypeBase,Response, UserBase, ShowUserBase
from typing import Annotated, Optional
from datetime import date
from model import Employee, EmployeeType, Users
from starlette.responses import RedirectResponse
import auth
import crud
import hash

router = APIRouter()
templates = Jinja2Templates(directory="template")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Employee Routers"""
@router.post('/employees/create')
async def create(request:Request,
                first_name: Annotated[str, Form()],
                last_name: Annotated[str, Form()],
                email: Annotated[str, Form()],
                employee_type: Annotated[int, Form()],
                benefits: Optional[str]=Form(None),
                leaves: Optional[int]=Form(None),
                project: Optional[str]=Form(None),
                contract_end: Optional[date]=Form(None),
                db:Session=Depends(get_db)):
    existing_employee = crud.get_employee_by_name(db,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  email=email
                                                  )
    if existing_employee:
        raise HTTPException(status_code=403, detail="Employee Record is already existing")
    create_employee = crud.create_employee(db, 
                        employee = {           
                         'first_name':first_name,
                         'last_name':last_name,
                         'email':email,
                         'employee_type':employee_type,
                         'benefits':benefits,
                         'leaves':leaves,
                         'project':project,
                         'contract_end':contract_end}
                         )
    # return Response(code="200",status="OK",message="Employee created successfully!").dict(exclude_none=True)
    # return templates.TemplateResponse("employees_create.html", {"request":request,"employees":_employee})
    return RedirectResponse(url="/employees",status_code=303)

@router.get('/employees/create_form')
def create_form(request:Request, db:Session = Depends(get_db)):
    employee_types = crud.get_employee_type(db)
    return templates.TemplateResponse("employee_create.html", {"request":request, "employee_types": employee_types})

@router.post('/employees/create_type')
async def create_type(request:EmployeeTypeBase,db:Session=Depends(get_db)):
    employee_type = crud.get_employee_type_by_desc(db,description=request.description)
    if employee_type:
        raise HTTPException(status_code=403, detail="Employee Type is already existing")
    create_employee_type = crud.create_employee_type(db, 
                         employee_type=request
                         )
    return Response(code="200",status="OK",message="Employee Type created successfully!").dict(exclude_none=True)
    # return templates.TemplateResponse("employees.html", {"request":request,"employees":_employee})

@router.get("/employees")
async def get(request:Request, db:Session=Depends(get_db)):
    current_employees = crud.get_employee(db,0,100)
    employee_types = crud.get_employee_type(db)
    # return Response(code="200", status="OK", message="Success fetch all data.", result=_book).dict(exclude_none=True)
    return templates.TemplateResponse("employees.html", {"request":request,"employees":current_employees,"employee_types": employee_types})

@router.get("/employees/employee_type")
async def get_all_employee_type(request:Request, db:Session=Depends(get_db)):
    employee_types = await crud.get_employee_type(db)

    # return Response(code="200", status="OK", message="Success fetch all data.", result=_employee_type).dict(exclude_none=True)
    return templates.TemplateResponse("employees.html", {"request":request,"employee_types": employee_types})

@router.get("/employees/{id}")
async def get_employee_by_id(request:Request,id:int,db:Session=Depends(get_db)):
    employee = crud.get_employee_by_id(db,id)
    employee_types = crud.get_employee_type(db)
    
    matching_types = [emp_type.description for emp_type in employee_types if emp_type.id == employee.employee_type]

    # return Response(code="200", status="OK", message="Success get data.", result=_employee).dict(exclude_none=True)
    return templates.TemplateResponse("employee_view_conditional.html", {"request":request,"employees":employee,"employee_types": employee_types,"desc":matching_types})

@router.get("/employees/{id}/update")
async def get_employee_by_id(request:Request,id:int,db:Session=Depends(get_db)):
    employee = crud.get_employee_by_id(db,id)
    employee_types = crud.get_employee_type(db)
    # return Response(code="200", status="OK", message="Success get data.", result=_employee).dict(exclude_none=True)
    return templates.TemplateResponse("employee_form.html", {"request":request,"employees":employee,"employee_types": employee_types})

@router.post("/employees/update/{id}/")
async def updating_employee(id:int,
                            request:Request,
                            first_name: Optional[str]=Form(None),
                            last_name: Optional[str]=Form(None),
                            email: Optional[str]=Form(None),
                            employee_type: Optional[int]=Form(None),
                            benefits: Optional[str]=Form(None),
                            leaves: Optional[int]=Form(None),
                            project: Optional[str]=Form(None),
                            contract_end: Optional[date]=Form(None), 
                            db:Session=Depends(get_db)):
    update_employee = crud.update_employee(db,
                            employee_id=id,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            employee_type=employee_type,
                            benefits=benefits,
                            leaves=leaves,
                            project=project,
                            contract_end=contract_end
                             )
    
    # return Response(code="200", status="OK", message="Success update data.", result=_employee)
    # return templates.TemplateResponse("employee_form.html", {"request":request,"employees":_employee})
    return RedirectResponse(url="/employees",status_code=303)

@router.post("/employees/delete/{id}")
async def delete_employee(request:Request,id:int,db:Session=Depends(get_db)):
    remove_employee = crud.remove_employee(db,employee_id=id)
    current_employee = crud.get_employee(db,0,100)
    employee_types = crud.get_employee_type(db)

    # return Response(code="200", status="OK", message="Success delete data.", result=_book).dict(exclude_none=True)
    # return templates.TemplateResponse("employees.html", {"request":request,"employees":current_employee,"employee_types": employee_types})
    return RedirectResponse(url="/employees",status_code=303)


"""User Routers"""
@router.post("/users", response_model=ShowUserBase, status_code=status.HTTP_201_CREATED)
def create_user(user : UserBase,db: Session = Depends(get_db)):
    user = Users(
        username = user.username,
        password = hash.Hasher.generate_password_hash(user.password),
        is_active = True,
        is_superuser = user.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

