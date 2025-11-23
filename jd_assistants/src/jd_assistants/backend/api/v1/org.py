from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from jd_assistants.database import get_session, DBDepartment,DBPosition
from jd_assistants.backend.api.v1.schemas import DepartmentCreate, DepartmentResponse, PositionCreate, PositionResponse
from jd_assistants.api_main import get_current_user

# Departments router
dept_router = APIRouter(prefix="/api/v1/departments", tags=["departments"])

@dept_router.post("/", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Create a new department"""
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_dept = DBDepartment(**department.dict())
    session.add(db_dept)
    await session.commit()
    await session.refresh(db_dept)
    return db_dept

@dept_router.get("/", response_model=List[DepartmentResponse])
async def list_departments(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """List all departments"""
    stmt = select(DBDepartment)
    result = await session.execute(stmt)
    departments = result.scalars().all()
    return departments

@dept_router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department(
    dept_id: int,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Get department by ID"""
    stmt = select(DBDepartment).where(DBDepartment.id == dept_id)
    result = await session.execute(stmt)
    dept = result.scalar_one_or_none()
    
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return dept

# Positions router
pos_router = APIRouter(prefix="/api/v1/positions", tags=["positions"])

@pos_router.post("/", response_model=PositionResponse)
async def create_position(
    position: PositionCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Create a new position"""
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_pos = DBPosition(**position.dict())
    session.add(db_pos)
    await session.commit()
    await session.refresh(db_pos)
    return db_pos

@pos_router.get("/", response_model=List[PositionResponse])
async def list_positions(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """List all positions"""
    stmt = select(DBPosition)
    result = await session.execute(stmt)
    positions = result.scalars().all()
    return positions

@pos_router.get("/{pos_id}", response_model=PositionResponse)
async def get_position(
    pos_id: int,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Get position by ID"""
    stmt = select(DBPosition).where(DBPosition.id == pos_id)
    result = await session.execute(stmt)
    pos = result.scalar_one_or_none()
    
    if not pos:
        raise HTTPException(status_code=404, detail="Position not found")
    
    return pos
