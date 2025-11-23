from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean, Date, Time, Enum
from datetime import datetime
import os
import enum

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://hr_user:hr_password@localhost:5432/hr_db")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Session factory
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
Base = declarative_base()

# Enums
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HR = "hr"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"

class ContractType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"

# ===== USERS & AUTH =====
class DBUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("DBEmployee", back_populates="user", uselist=False)

# ===== DEPARTMENTS & POSITIONS =====
class DBDepartment(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    head_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employees = relationship("DBEmployee", back_populates="department", foreign_keys="DBEmployee.department_id")
    
class DBPosition(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    level = Column(String)
    salary_range_min = Column(Float)
    salary_range_max = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employees = relationship("DBEmployee", back_populates="position")

# ===== EMPLOYEES =====
class DBEmployee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    employee_code = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String)
    phone = Column(String)
    address = Column(Text)
    
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    join_date = Column(Date, nullable=False)
    contract_type = Column(Enum(ContractType), default=ContractType.FULL_TIME)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("DBUser", back_populates="employee")
    department = relationship("DBDepartment", back_populates="employees", foreign_keys=[department_id])
    position = relationship("DBPosition", back_populates="employees")

# ===== CANDIDATES (Keep existing for recruitment) =====
class DBCandidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    bio = Column(Text)
    skills = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DBJobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    skills = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Integer, default=1)

class DBCandidateScore(Base):
    __tablename__ = "candidate_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, index=True)
    name = Column(String)
    score = Column(Integer)
    reason = Column(Text)
    jd_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    """Get database session"""
    async with async_session_maker() as session:
        yield session

# CRUD Operations (keep existing + add new)
from sqlalchemy import select

async def create_user(session: AsyncSession, email: str, password_hash: str, role: UserRole = UserRole.EMPLOYEE):
    """Create a new user"""
    user = DBUser(email=email, password_hash=password_hash, role=role)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_email(session: AsyncSession, email: str):
    """Get user by email"""
    stmt = select(DBUser).where(DBUser.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_employee(session: AsyncSession, employee_data: dict):
    """Create a new employee"""
    employee = DBEmployee(**employee_data)
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee

async def get_all_employees(session: AsyncSession):
    """Get all employees"""
    stmt = select(DBEmployee).order_by(DBEmployee.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()

# Keep existing candidate operations
async def create_candidate(session: AsyncSession, candidate_data: dict):
    """Create a new candidate"""
    stmt = select(DBCandidate).where(DBCandidate.candidate_id == candidate_data["id"])
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.name = candidate_data["name"]
        existing.email = candidate_data["email"]
        existing.bio = candidate_data["bio"]
        existing.skills = candidate_data["skills"]
        existing.updated_at = datetime.utcnow()
        await session.commit()
        return existing
    else:
        db_candidate = DBCandidate(
            candidate_id=candidate_data["id"],
            name=candidate_data["name"],
            email=candidate_data["email"],
            bio=candidate_data["bio"],
            skills=candidate_data["skills"]
        )
        session.add(db_candidate)
        await session.commit()
        await session.refresh(db_candidate)
        return db_candidate
