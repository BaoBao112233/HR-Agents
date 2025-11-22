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


class Skill(BaseModel):
    name: str
    levels: int
    descriptions: str


class CandidateProfile(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    work_experience: List[WorkExperience]
    skills: List[Skill]

