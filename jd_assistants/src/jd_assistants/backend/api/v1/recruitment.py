"""
Recruitment API endpoints for CV and JD management
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pathlib import Path
import os
from datetime import datetime

from jd_assistants.database import (
    get_session,
    get_all_candidates, get_candidate_by_id, delete_candidate,
    get_all_jds, get_jd_by_id, create_job_description,
    update_jd, delete_jd, activate_jd, get_active_jd,
    save_candidate_score, get_candidate_scores, get_scores_by_jd,
    create_candidate
)

# Import agents from app.py
from jd_assistants.inference.groq import ChatGroq
from jd_assistants.agent.read_cv import ReadCVAgent
from jd_assistants.agent.summarization import SummarizationAgent
from jd_assistants.agent.score import ScoreAgent
from jd_assistants.agent.jd_rewriter import JDRewriterAgent
from jd_assistants.tools.read_pdf_tool import ReadPDFTool
from jd_assistants.models import Candidate

# Initialize LLM and agents
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not set")

llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
read_cv_agent = ReadCVAgent(llm)
summarization_agent = SummarizationAgent(llm)
score_agent = ScoreAgent(llm)
jd_rewriter_agent = JDRewriterAgent(llm)
read_pdf_tool = ReadPDFTool()

# Upload directory
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/api/v1", tags=["recruitment"])

# ===== CANDIDATES ENDPOINTS =====

@router.post("/candidates/upload-cv")
async def upload_cvs(
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session)
):
    """Upload and process CV files"""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    results = []
    errors = []
    
    for idx, file in enumerate(files):
        try:
            # Validate file type
            if not file.filename.endswith('.pdf'):
                errors.append(f"{file.filename}: Only PDF files are supported")
                continue
            
            # Save file
            file_path = UPLOAD_DIR / f"{datetime.utcnow().timestamp()}_{file.filename}"
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Process CV
            pdf_content = read_pdf_tool._run(str(file_path))
            extracted_data = read_cv_agent.process(pdf_content, file.filename)
            
            # Extract data
            name = extracted_data.get("personal_info", {}).get("name", "Unknown")
            email = extracted_data.get("personal_info", {}).get("email", "")
            skills_list = extracted_data.get("skills", [])
            skills = ", ".join([s.get("name", "") for s in skills_list if isinstance(s, dict)])
            
            # Summarize
            candidate_info = {
                "name": name,
                "education": extracted_data.get("education"),
                "work_experience": extracted_data.get("work_experience"),
                "skills": skills
            }
            bio = summarization_agent.process(candidate_info)
            
            # Save to database
            candidate_data = {
                "id": f"cand_{int(datetime.utcnow().timestamp())}_{idx}",
                "name": name,
                "email": email,
                "bio": bio,
                "skills": skills
            }
            await create_candidate(session, candidate_data)
            
            results.append({
                "filename": file.filename,
                "name": name,
                "email": email,
                "status": "success"
            })
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    return {
        "success": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }

@router.get("/candidates")
async def list_candidates(session: AsyncSession = Depends(get_session)):
    """Get all candidates"""
    candidates = await get_all_candidates(session)
    return [{
        "id": c.candidate_id,
        "name": c.name,
        "email": c.email,
        "bio": c.bio,
        "skills": c.skills,
        "created_at": c.created_at.isoformat()
    } for c in candidates]

@router.get("/candidates/{candidate_id}")
async def get_candidate(candidate_id: str, session: AsyncSession = Depends(get_session)):
    """Get candidate by ID"""
    candidate = await get_candidate_by_id(session, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {
        "id": candidate.candidate_id,
        "name": candidate.name,
        "email": candidate.email,
        "bio": candidate.bio,
        "skills": candidate.skills,
        "created_at": candidate.created_at.isoformat()
    }

@router.delete("/candidates/{candidate_id}")
async def remove_candidate(candidate_id: str, session: AsyncSession = Depends(get_session)):
    """Delete a candidate"""
    success = await delete_candidate(session, candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully"}

# ===== JOB DESCRIPTION ENDPOINTS =====

@router.get("/job-descriptions")
async def list_job_descriptions(session: AsyncSession = Depends(get_session)):
    """Get all job descriptions"""
    jds = await get_all_jds(session)
    return [{
        "id": jd.id,
        "title": jd.title,
        "description": jd.description,
        "skills": jd.skills,
        "is_active": bool(jd.is_active),
        "created_at": jd.created_at.isoformat()
    } for jd in jds]

@router.post("/job-descriptions")
async def create_jd(
    title: str = Form(...),
    description: str = Form(...),
    skills: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """Create a new job description"""
    jd_data = {
        "title": title,
        "description": description,
        "skills": skills,
        "is_active": 0
    }
    jd = await create_job_description(session, jd_data)
    return {
        "id": jd.id,
        "title": jd.title,
        "description": jd.description,
        "skills": jd.skills,
        "is_active": bool(jd.is_active),
        "created_at": jd.created_at.isoformat()
    }

@router.get("/job-descriptions/{jd_id}")
async def get_jd(jd_id: int, session: AsyncSession = Depends(get_session)):
    """Get job description by ID"""
    jd = await get_jd_by_id(session, jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {
        "id": jd.id,
        "title": jd.title,
        "description": jd.description,
        "skills": jd.skills,
        "is_active": bool(jd.is_active),
        "created_at": jd.created_at.isoformat()
    }

@router.put("/job-descriptions/{jd_id}")
async def update_job_description(
    jd_id: int,
    title: str = Form(...),
    description: str = Form(...),
    skills: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """Update a job description"""
    jd_data = {
        "title": title,
        "description": description,
        "skills": skills
    }
    jd = await update_jd(session, jd_id, jd_data)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {
        "id": jd.id,
        "title": jd.title,
        "description": jd.description,
        "skills": jd.skills,
        "is_active": bool(jd.is_active)
    }

@router.delete("/job-descriptions/{jd_id}")
async def remove_jd(jd_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a job description"""
    success = await delete_jd(session, jd_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {"message": "Job description deleted successfully"}

@router.put("/job-descriptions/{jd_id}/activate")
async def set_active_jd(jd_id: int, session: AsyncSession = Depends(get_session)):
    """Set a job description as active"""
    jd = await activate_jd(session, jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {
        "id": jd.id,
        "title": jd.title,
        "is_active": True,
        "message": "Job description activated successfully"
    }

# ===== SCORING ENDPOINTS =====

@router.post("/scoring/score-all")
async def score_all_candidates(session: AsyncSession = Depends(get_session)):
    """Score all candidates against active JD"""
    # Get active JD
    jd = await get_active_jd(session)
    if not jd:
        raise HTTPException(status_code=400, detail="No active job description found")
    
    # Get all candidates
    candidates = await get_all_candidates(session)
    if not candidates:
        raise HTTPException(status_code=400, detail="No candidates found")
    
    results = []
    for candidate in candidates:
        cand_obj = Candidate(
            id=candidate.candidate_id,
            name=candidate.name,
            email=candidate.email,
            bio=candidate.bio,
            skills=candidate.skills
        )
        
        score_data = score_agent.process(cand_obj, jd.description, jd.skills)
        
        if isinstance(score_data, dict):
            await save_candidate_score(session, score_data, jd.id)
            results.append({
                "name": candidate.name,
                "score": score_data.get("score", 0),
                "reason": score_data.get("reason", "")
            })
    
    return {
        "jd_id": jd.id,
        "jd_title": jd.title,
        "total_scored": len(results),
        "results": sorted(results, key=lambda x: x["score"], reverse=True)
    }

@router.get("/scoring/scores")
async def get_scores(
    jd_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session)
):
    """Get candidate scores, optionally filtered by JD"""
    scores = await get_candidate_scores(session, jd_id)
    return [{
        "id": s.id,
        "candidate_id": s.candidate_id,
        "name": s.name,
        "score": s.score,
        "reason": s.reason,
        "jd_id": s.jd_id,
        "created_at": s.created_at.isoformat()
    } for s in scores]

# ===== JD AI ENDPOINTS =====

@router.post("/jd-ai/analyze")
async def analyze_jd(jd_text: str = Form(...)):
    """Analyze JD and provide suggestions"""
    if not jd_text:
        raise HTTPException(status_code=400, detail="JD text is required")
    
    analysis = jd_rewriter_agent.analyze_jd(jd_text)
    
    if isinstance(analysis, dict):
        return {
            "overall_score": analysis.get("overall_score", 0),
            "key_recommendations": analysis.get("key_recommendations", []),
            "improvements": analysis.get("improvements", [])[:5],  # Top 5
            "success": True
        }
    
    return {"success": False, "error": "Failed to analyze JD"}

@router.post("/jd-ai/rewrite")
async def rewrite_jd(jd_text: str = Form(...)):
    """Rewrite complete JD using AI"""
    if not jd_text:
        raise HTTPException(status_code=400, detail="JD text is required")
    
    rewritten = jd_rewriter_agent.rewrite_jd(jd_text)
    
    return {
        "original": jd_text,
        "rewritten": rewritten,
        "success": True
    }

@router.post("/jd-ai/generate")
async def generate_jd_from_requirements(
    position: str = Form(...),
    experience_years: int = Form(...),
    required_skills: str = Form(...),
    salary_range: str = Form(...),
    job_type: str = Form(default="Full-time"),
    location: str = Form(default=""),
    benefits: str = Form(default=""),
    language: str = Form(default="en")  # NEW: language parameter
):
    """Generate professional JD from requirements using AI"""
    
    # Language instruction
    lang_instruction = ""
    if language == "vi":
        lang_instruction = "\n\nIMPORTANT: Write the ENTIRE job description in Vietnamese (Tiếng Việt). All sections, headings, and content must be in Vietnamese.\n\n"
    else:
        lang_instruction = "\n\nIMPORTANT: Write the ENTIRE job description in English.\n\n"
    
    # Build prompt for JD generation
    prompt = f"""{lang_instruction}Generate a professional, detailed job description for the following position:

Position: {position}
Experience Required: {experience_years} years
Required Skills: {required_skills}
Salary Range: {salary_range}
Job Type: {job_type}
Location: {location if location else "Remote/Flexible"}
Benefits: {benefits if benefits else "Competitive benefits package"}

Create a complete job description with these sections:

# {position}

## Overview
[Write an engaging 2-3 sentence overview of the role and company]

## Key Responsibilities
[List 6-8 specific responsibilities, each starting with an action verb]

## Required Qualifications
- {experience_years}+ years of experience in relevant field
- Strong proficiency in: {required_skills}
[Add 3-4 more specific qualifications]

## Preferred Qualifications
[List 3-4 nice-to-have skills or experiences]

## Technical Skills
[Expand on required skills with specific tools, frameworks, or methodologies]

## What We Offer
- Competitive salary: {salary_range}
- {benefits if benefits else "Comprehensive benefits package including health insurance, retirement plans, and professional development opportunities"}
[Add 3-4 more specific benefits]

## About Us
[Write a brief, inspiring paragraph about the company culture and mission]

Make it professional, detailed, and attractive to top candidates. Use clear, professional language."""

    try:
        # Use LLM to generate JD
        response = llm.invoke(prompt)
        generated_jd = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "success": True,
            "generated_jd": generated_jd,
            "inputs": {
                "position": position,
                "experience_years": experience_years,
                "skills": required_skills,
                "salary_range": salary_range,
                "job_type": job_type,
                "location": location
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate JD: {str(e)}")

@router.post("/jd-ai/assess-salary")
async def assess_salary_competitiveness(
    position: str = Form(...),
    experience_years: int = Form(...),
    salary_offered: str = Form(...),
    location: str = Form(default="Vietnam"),
    required_skills: str = Form(default=""),
    language: str = Form(default="en")  # NEW: language parameter
):
    """Assess salary competitiveness using AI and market knowledge"""
    
    # Language instruction
    lang_instruction = ""
    if language == "vi":
        lang_instruction = "\n\nIMPORTANT: Provide your analysis in Vietnamese (Tiếng Việt). The 'insights' field should be in Vietnamese, and recommendations should be in Vietnamese as well.\n\n"
    else:
        lang_instruction = "\n\nIMPORTANT: Provide your analysis in English.\n\n"
    
    # Build prompt for salary assessment  
    prompt = f"""{lang_instruction}Analyze the salary competitiveness for this position:

Position: {position}
Experience Level: {experience_years} years
Salary Offered: {salary_offered}
Location: {location}
Required Skills: {required_skills}

Based on current market data and industry standards, provide a comprehensive salary assessment:

1. MARKET ANALYSIS
   - Estimate the typical salary range for this position with {experience_years} years of experience in {location}
   - Consider the skill requirements: {required_skills}
   
2. COMPETITIVENESS ASSESSMENT
   - Rate as: "highly_competitive" (top 25%), "competitive" (market rate), "below_market" (bottom 25%), or "significantly_below" (bottom 10%)
   - Provide a numerical score from 0-100 where:
     * 90-100: Highly competitive, will attract top talent
     * 70-89: Competitive, aligned with market
     * 50-69: Slightly below market
     * 30-49: Below market, may struggle to attract talent
     * 0-29: Significantly below market

3. KEY INSIGHTS
   - What makes this salary offer competitive or not?
   - How does location affect this assessment?
   - Impact of required skills on market value
   
4. RECOMMENDATIONS
   - If below market: Suggest specific adjustments
   - If competitive: Suggest other ways to make offer attractive
   - If above market: Confirm this is intentional for top talent

Return your analysis as a structured JSON with these exact keys:
{{
    "market_range_min": [number],
    "market_range_max": [number],
    "assessment": "[highly_competitive|competitive|below_market|significantly_below]",
    "score": [0-100],
    "insights": "[detailed analysis paragraph]",
    "recommendations": ["recommendation 1", "recommendation 2", "recommendation 3"]
}}

Be realistic and data-driven in your assessment."""

    try:
        # Use LLM for salary assessment
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        # Try to parse JSON from response
        import json
        import re
        
        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object in response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            json_str = json_match.group(0) if json_match else content
        
        try:
            analysis = json.loads(json_str)
        except:
            # If JSON parsing fails, create structured response from text
            analysis = {
                "market_range_min": 0,
                "market_range_max": 0,
                "assessment": "competitive",
                "score": 75,
                "insights": content,
                "recommendations": ["Review detailed analysis above"]
            }
        
        return {
            "success": True,
            "assessment": analysis.get("assessment", "competitive"),
            "score": analysis.get("score", 75),
            "market_range": f"${analysis.get('market_range_min', 0):,} - ${analysis.get('market_range_max', 0):,}",
            "insights": analysis.get("insights", "Analysis completed"),
            "recommendations": analysis.get("recommendations", []),
            "inputs": {
                "position": position,
                "experience_years": experience_years,
                "salary_offered": salary_offered,
                "location": location
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assess salary: {str(e)}")
