from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Employee schemas
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    join_date: date
    contract_type: str = "full_time"

class EmployeeCreate(EmployeeBase):
    password: str  # For creating user account

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    status: Optional[str] = None

class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    department_id: Optional[int]
    position_id: Optional[int]
    join_date: date
    status: str
    
    class Config:
        from_attributes = True

# Department schemas
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    parent_id: Optional[int]
    head_id: Optional[int]
    
    class Config:
        from_attributes = True

# Position schemas
class PositionBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None

class PositionCreate(PositionBase):
    pass

class PositionResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    level: Optional[str]
    salary_range_min: Optional[float]
    salary_range_max: Optional[float]
    
    class Config:
        from_attributes = True
