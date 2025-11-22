from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from datetime import datetime
import os

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://hr_user:hr_password@localhost:5432/hr_db")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Session factory
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
Base = declarative_base()

# Database Models
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
    is_active = Column(Integer, default=1)  # Boolean as integer

class DBCandidateScore(Base):
    __tablename__ = "candidate_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, index=True)
    name = Column(String)
    score = Column(Integer)
    reason = Column(Text)
    jd_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database operations
async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    """Get database session"""
    async with async_session_maker() as session:
        yield session

# CRUD Operations
async def create_candidate(session: AsyncSession, candidate_data: dict):
    """Create a new candidate"""
    from sqlalchemy import select
    
    # Check if candidate already exists
    stmt = select(DBCandidate).where(DBCandidate.candidate_id == candidate_data["id"])
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing
        existing.name = candidate_data["name"]
        existing.email = candidate_data["email"]
        existing.bio = candidate_data["bio"]
        existing.skills = candidate_data["skills"]
        existing.updated_at = datetime.utcnow()
        await session.commit()
        return existing
    else:
        # Create new
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

async def get_all_candidates(session: AsyncSession):
    """Get all candidates"""
    from sqlalchemy import select
    stmt = select(DBCandidate).order_by(DBCandidate.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_job_description(session: AsyncSession, jd_data: dict):
    """Create or update job description"""
    from sqlalchemy import select, update
    
    # Deactivate all previous JDs
    await session.execute(
        update(DBJobDescription).values(is_active=0)
    )
    
    # Create new active JD
    db_jd = DBJobDescription(
        title=jd_data.get("title", "Job Description"),
        description=jd_data["description"],
        skills=jd_data["skills"],
        is_active=1
    )
    session.add(db_jd)
    await session.commit()
    await session.refresh(db_jd)
    return db_jd

async def get_active_jd(session: AsyncSession):
    """Get active job description"""
    from sqlalchemy import select
    stmt = select(DBJobDescription).where(DBJobDescription.is_active == 1).order_by(DBJobDescription.created_at.desc())
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def save_candidate_score(session: AsyncSession, score_data: dict, jd_id: int):
    """Save candidate score"""
    db_score = DBCandidateScore(
        candidate_id=score_data["id"],
        name=score_data["name"],
        score=score_data["score"],
        reason=score_data["reason"],
        jd_id=jd_id
    )
    session.add(db_score)
    await session.commit()
    await session.refresh(db_score)
    return db_score

async def get_candidate_scores(session: AsyncSession, jd_id: int = None):
    """Get candidate scores"""
    from sqlalchemy import select
    stmt = select(DBCandidateScore)
    if jd_id:
        stmt = stmt.where(DBCandidateScore.jd_id == jd_id)
    stmt = stmt.order_by(DBCandidateScore.score.desc())
    result = await session.execute(stmt)
    return result.scalars().all()
