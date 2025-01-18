from pydantic import BaseModel
from typing import List, Optional


class JobDescription(BaseModel):
    title: str
    description: str
    skills: str


class Candidate(BaseModel):
    id: str
    name: str
    email: str
    bio: str
    skills: str


class CandidateScore(BaseModel):
    id: str
    name: str
    score: int
    reason: str


class ScoredCandidate(BaseModel):
    id: str
    name: str
    email: str
    bio: str
    skills: str
    score: int
    reason: str


class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    job_title: str
    dob: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    address: str


class Education(BaseModel):
    university: str
    major: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class WorkExperience(BaseModel):
    company: str
    position: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class Course(BaseModel):
    name: str
    organization: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class Project(BaseModel):
    name: str
    customer: str
    num_members: int
    position: str
    tasks: str
    technologies: List[str]
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class Product(BaseModel):
    name: str
    class_name: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class Skill(BaseModel):
    name: str
    levels: int
    descriptions: str


class Certificate(BaseModel):
    organization: str
    name: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class Award(BaseModel):
    organization: str
    name: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class Activity(BaseModel):
    organization: str
    position: str
    start_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    end_date: str  # định dạng: yyyy hoặc yyyy-mm hoặc yyyy-mm-dd
    descriptions: str


class CandidateProfile(BaseModel):
    personal_info: PersonalInfo
    additional_info: Optional[str]
    education: List[Education]
    work_experience: List[WorkExperience]
    courses: List[Course]
    projects: List[Project]
    products: List[Product]
    skills: List[Skill]
    certificate: List[Certificate]
    awards: List[Award]
    activities: List[Activity]

