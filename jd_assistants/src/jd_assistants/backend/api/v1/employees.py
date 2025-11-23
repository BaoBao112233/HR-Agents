from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import random
import string

from jd_assistants.database import get_session, DBEmployee, create_employee, get_all_employees, create_user, UserRole
from jd_assistants.backend.api.v1.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from jd_assistants.auth import get_password_hash
from jd_assistants.api_main import get_current_user

router = APIRouter(prefix="/api/v1/employees", tags=["employees"])

def generate_employee_code():
    """Generate unique employee code"""
    return "EMP" + ''.join(random.choices(string.digits, k=6))

@router.post("/", response_model=EmployeeResponse)
async def create_employee_endpoint(
    employee: EmployeeCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Create a new employee"""
    # Only HR and Admin can create employees
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Create user account first
    password_hash = get_password_hash(employee.password)
    user = await create_user(session, employee.email, password_hash, UserRole.EMPLOYEE)
    
    # Create employee record
    employee_data = {
        "user_id": user.id,
        "employee_code": generate_employee_code(),
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "date_of_birth": employee.date_of_birth,
        "gender": employee.gender,
        "phone": employee.phone,
        "address": employee.address,
        "department_id": employee.department_id,
        "position_id": employee.position_id,
        "manager_id": employee.manager_id,
        "join_date": employee.join_date,
        "contract_type": employee.contract_type,
        "status": "active"
    }
    
    db_employee = await create_employee(session, employee_data)
    return db_employee

@router.get("/", response_model=List[EmployeeResponse])
async def list_employees(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """List all employees"""
    employees = await get_all_employees(session)
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Get employee by ID"""
    stmt = select(DBEmployee).where(DBEmployee.id == employee_id)
    result = await session.execute(stmt)
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(
    employee_id: int,
    employee_update: EmployeeUpdate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Update employee information"""
    # Only HR, Admin, or the employee themselves can update
    stmt = select(DBEmployee).where(DBEmployee.id == employee_id)
    result = await session.execute(stmt)
    db_employee = result.scalar_one_or_none()
    
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check authorization
    if current_user.role not in ["hr", "admin"] and db_employee.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    update_data = employee_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    await session.commit()
    await session.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Delete (deactivate) an employee"""
    # Only HR and Admin can delete
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    stmt = select(DBEmployee).where(DBEmployee.id == employee_id)
    result = await session.execute(stmt)
    db_employee = result.scalar_one_or_none()
    
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Soft delete by changing status
    db_employee.status = "terminated"
    await session.commit()
    
    return {"message": "Employee deactivated successfully"}
