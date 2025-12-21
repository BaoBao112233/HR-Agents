"""
Recruitment API endpoints for CV and JD management - ClickHouse version
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Header
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
from pathlib import Path
import os
from datetime import datetime
import json
import asyncio

from jd_assistants.clickhouse_db import (
    get_all_candidates, get_candidate_by_id, delete_candidate,
    get_all_jds, get_jd_by_id, create_job_description,
    update_jd, delete_jd, activate_jd, get_active_jd,
    save_candidate_score, get_scores_by_jd,
    create_candidate, get_active_api_key
)

# Import agents
from jd_assistants.inference.llm_factory import create_llm, get_default_model
from jd_assistants.agent.read_cv import ReadCVAgent
from jd_assistants.agent.summarization import SummarizationAgent
from jd_assistants.agent.score import ScoreAgent
from jd_assistants.agent.jd_rewriter import JDRewriterAgent
from jd_assistants.agent.jd_analysis import JDAnalysisAgent
from jd_assistants.tools.read_pdf_tool import ReadPDFTool
from jd_assistants.models import Candidate

# Upload directory
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/api/v1", tags=["recruitment"])


# Dependency to get current user ID (placeholder)
async def get_current_user_id() -> str:
    # TODO: Replace with actual authentication
    return "user_1"


def get_llm_for_user(user_id: str, provider: str = None):
    """Get LLM instance for user based on their API keys"""
    # If provider not specified, try to get from environment or use default
    if not provider:
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "groq")
    
    # Try to get API key from database
    api_key = get_active_api_key(user_id, provider)
    
    # Fallback to environment variable if no key in database
    if not api_key:
        env_var = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var)
    
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail=f"No API key found for provider: {provider}. Please add an API key in settings."
        )
    
    # Get model from environment or use default
    model = os.getenv(f"{provider.upper()}_MODEL") or get_default_model(provider)
    
    # Create LLM instance
    return create_llm(provider, model, api_key, temperature=0)


# ===== CANDIDATES ENDPOINTS =====

@router.post("/candidates/upload-cv")
async def upload_cvs(
    files: List[UploadFile] = File(...),
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Upload and process CV files"""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Get LLM for processing
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    # Initialize agents
    read_cv_agent = ReadCVAgent(llm)
    summarization_agent = SummarizationAgent(llm)
    read_pdf_tool = ReadPDFTool()
    
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
            personal_info = extracted_data.get("personal_info", {})
            name = personal_info.get("name", "Unknown")
            email = personal_info.get("email", "")
            phone = personal_info.get("phone", "")
            
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
                "candidate_id": f"cand_{int(datetime.utcnow().timestamp() * 1000)}_{idx}",
                "name": name,
                "email": email,
                "phone": phone,
                "bio": bio,
                "skills": skills,
                "personal_info": personal_info,
                "education": extracted_data.get("education", []),
                "work_experience": extracted_data.get("work_experience", []),
                "cv_file_path": str(file_path)
            }
            create_candidate(candidate_data)
            
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
async def list_candidates():
    """Get all candidates"""
    candidates = get_all_candidates()
    return [{
        "id": c["candidate_id"],
        "name": c["name"],
        "email": c["email"],
        "phone": c.get("phone", ""),
        "bio": c["bio"],
        "skills": c["skills"],
        "created_at": c["created_at"].isoformat() if isinstance(c["created_at"], datetime) else c["created_at"]
    } for c in candidates]


@router.get("/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    """Get candidate by ID"""
    candidate = get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {
        "id": candidate["candidate_id"],
        "name": candidate["name"],
        "email": candidate["email"],
        "phone": candidate.get("phone", ""),
        "bio": candidate["bio"],
        "skills": candidate["skills"],
        "personal_info": candidate.get("personal_info", {}),
        "education": candidate.get("education", []),
        "work_experience": candidate.get("work_experience", []),
        "created_at": candidate["created_at"].isoformat() if isinstance(candidate["created_at"], datetime) else candidate["created_at"]
    }


@router.delete("/candidates/{candidate_id}")
async def remove_candidate(candidate_id: str):
    """Delete a candidate"""
    success = delete_candidate(candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully"}


# ===== JOB DESCRIPTION ENDPOINTS =====

@router.get("/job-descriptions")
async def list_job_descriptions():
    """Get all job descriptions"""
    jds = get_all_jds()
    return [{
        "id": jd["id"],
        "title": jd["title"],
        "description": jd["description"],
        "skills": jd["skills"],
        "requirements": jd.get("requirements", ""),
        "benefits": jd.get("benefits", ""),
        "is_active": jd["is_active"],
        "created_at": jd["created_at"].isoformat() if isinstance(jd["created_at"], datetime) else jd["created_at"]
    } for jd in jds]


@router.post("/job-descriptions")
async def create_jd(
    title: str = Form(...),
    description: str = Form(...),
    skills: str = Form(...),
    requirements: str = Form(default=""),
    benefits: str = Form(default=""),
    user_id: str = Depends(get_current_user_id)
):
    """Create a new job description"""
    jd_data = {
        "title": title,
        "description": description,
        "skills": skills,
        "requirements": requirements,
        "benefits": benefits,
        "is_active": 0,
        "created_by": user_id
    }
    jd = create_job_description(jd_data)
    return {
        "id": jd["id"],
        "title": jd["title"],
        "description": jd["description"],
        "skills": jd["skills"],
        "requirements": jd.get("requirements", ""),
        "benefits": jd.get("benefits", ""),
        "is_active": jd["is_active"],
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/job-descriptions/{jd_id}")
async def get_jd(jd_id: str):
    """Get job description by ID"""
    jd = get_jd_by_id(jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {
        "id": jd["id"],
        "title": jd["title"],
        "description": jd["description"],
        "skills": jd["skills"],
        "requirements": jd.get("requirements", ""),
        "benefits": jd.get("benefits", ""),
        "is_active": jd["is_active"],
        "created_at": jd["created_at"].isoformat() if isinstance(jd["created_at"], datetime) else jd["created_at"]
    }


@router.put("/job-descriptions/{jd_id}")
async def update_job_description(
    jd_id: str,
    title: str = Form(default=None),
    description: str = Form(default=None),
    skills: str = Form(default=None),
    requirements: str = Form(default=None),
    benefits: str = Form(default=None)
):
    """Update a job description"""
    jd_data = {}
    if title:
        jd_data["title"] = title
    if description:
        jd_data["description"] = description
    if skills:
        jd_data["skills"] = skills
    if requirements:
        jd_data["requirements"] = requirements
    if benefits:
        jd_data["benefits"] = benefits
    
    success = update_jd(jd_id, jd_data)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    jd = get_jd_by_id(jd_id)
    return {
        "id": jd["id"],
        "title": jd["title"],
        "description": jd["description"],
        "skills": jd["skills"],
        "is_active": jd["is_active"]
    }


@router.delete("/job-descriptions/{jd_id}")
async def remove_jd(jd_id: str):
    """Delete a job description"""
    success = delete_jd(jd_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {"message": "Job description deleted successfully"}


@router.put("/job-descriptions/{jd_id}/activate")
async def set_active_jd(jd_id: str):
    """Set a job description as active"""
    success = activate_jd(jd_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    jd = get_jd_by_id(jd_id)
    return {
        "id": jd["id"],
        "title": jd["title"],
        "is_active": True,
        "message": "Job description activated successfully"
    }


# ===== SCORING ENDPOINTS =====

@router.post("/scoring/score-all")
async def score_all_candidates(
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Score all candidates against active JD"""
    # Get active JD
    jd = get_active_jd()
    if not jd:
        raise HTTPException(status_code=400, detail="No active job description found")
    
    # Get all candidates
    candidates = get_all_candidates()
    if not candidates:
        raise HTTPException(status_code=400, detail="No candidates found")
    
    # Get LLM
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    score_agent = ScoreAgent(llm)
    
    results = []
    for candidate in candidates:
        cand_obj = Candidate(
            id=candidate["candidate_id"],
            name=candidate["name"],
            email=candidate["email"],
            bio=candidate["bio"],
            skills=candidate["skills"]
        )
        
        score_data = score_agent.process(cand_obj, jd["description"], jd["skills"])
        
        if isinstance(score_data, dict):
            save_candidate_score({
                "candidate_id": candidate["candidate_id"],
                "jd_id": jd["id"],
                "score": score_data.get("score", 0),
                "reason": score_data.get("reason", "")
            })
            results.append({
                "name": candidate["name"],
                "score": score_data.get("score", 0),
                "reason": score_data.get("reason", "")
            })
    
    return {
        "jd_id": jd["id"],
        "jd_title": jd["title"],
        "total_scored": len(results),
        "results": sorted(results, key=lambda x: x["score"], reverse=True)
    }


@router.get("/scoring/scores")
async def get_scores(jd_id: Optional[str] = None):
    """Get candidate scores, optionally filtered by JD"""
    if jd_id:
        scores = get_scores_by_jd(jd_id)
    else:
        # Get active JD scores
        jd = get_active_jd()
        if jd:
            scores = get_scores_by_jd(jd["id"])
        else:
            scores = []
    
    return [{
        "id": s["id"],
        "candidate_id": s["candidate_id"],
        "candidate_name": s.get("candidate_name", ""),
        "score": s["score"],
        "reason": s["reason"],
        "jd_id": s["jd_id"],
        "scored_at": s["scored_at"].isoformat() if isinstance(s["scored_at"], datetime) else s["scored_at"]
    } for s in scores]


# ===== JD ANALYSIS ENDPOINTS (NEW) =====

@router.post("/jd-ai/analyze")
async def analyze_jd(
    jd_text: str = Form(...),
    language: str = Form(default="en"),
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Analyze JD and provide evaluation"""
    if not jd_text:
        raise HTTPException(status_code=400, detail="JD text is required")
    
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    jd_analysis_agent = JDAnalysisAgent(llm)
    analysis = jd_analysis_agent.analyze(jd_text, language)
    
    if isinstance(analysis, dict):
        return {
            "overall_score": analysis.get("overall_score", 0),
            "key_recommendations": analysis.get("key_recommendations", []),
            "improvements": analysis.get("improvements", [])[:5],
            "success": True
        }
    
    return {"success": False, "error": "Failed to analyze JD"}


@router.post("/jd-ai/analyze-stream")
async def analyze_jd_stream(
    jd_text: str = Form(...),
    language: str = Form(default="en"),
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Analyze JD with streaming response"""
    if not jd_text:
        raise HTTPException(status_code=400, detail="JD text is required")
    
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    jd_analysis_agent = JDAnalysisAgent(llm)
    
    async def event_generator():
        try:
            async for chunk in jd_analysis_agent.astream_analyze(jd_text, language):
                if chunk.get("type") == "progress":
                    event_data = {
                        "type": "thinking",
                        "content": chunk.get("content", ""),
                        "accumulated": chunk.get("accumulated", "")
                    }
                elif chunk.get("type") == "final":
                    data = chunk.get("data")
                    if data:
                        event_data = {
                            "type": "final",
                            "data": {
                                "thinking": data.thinking,
                                "overall_score": data.overall_score,
                                "key_recommendations": data.key_recommendations,
                                "improvements": [
                                    {
                                        "section": imp.section,
                                        "original": imp.original,
                                        "improved": imp.improved,
                                        "reason": imp.reason
                                    } for imp in data.improvements[:5]
                                ]
                            }
                        }
                    else:
                        event_data = {"type": "error", "error": "No data in final chunk"}
                elif chunk.get("type") == "error":
                    event_data = {
                        "type": "error",
                        "error": chunk.get("error", "Unknown error"),
                        "raw_content": chunk.get("raw_content", "")
                    }
                else:
                    continue
                
                yield f"data: {json.dumps(event_data)}\n\n"
        except Exception as e:
            import traceback
            error_data = {
                "type": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# ===== JD REWRITING ENDPOINTS =====

@router.post("/jd-ai/rewrite")
async def rewrite_jd(
    jd_text: str = Form(...),
    language: str = Form(default="en"),
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Rewrite complete JD using AI"""
    if not jd_text:
        raise HTTPException(status_code=400, detail="JD text is required")
    
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    jd_rewriter_agent = JDRewriterAgent(llm)
    rewritten = jd_rewriter_agent.rewrite_jd(jd_text, language)
    
    return {
        "original": jd_text,
        "rewritten": rewritten,
        "success": True
    }


@router.post("/jd-ai/rewrite-stream")
async def rewrite_jd_stream(
    jd_text: str = Form(...),
    language: str = Form(default="en"),
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Rewrite JD with streaming response"""
    if not jd_text:
        raise HTTPException(status_code=400, detail="JD text is required")
    
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    jd_rewriter_agent = JDRewriterAgent(llm)
    
    async def event_generator():
        try:
            async for chunk in jd_rewriter_agent.astream_rewrite_jd(jd_text, language=language):
                if chunk.get("type") == "progress":
                    event_data = {
                        "type": "thinking",
                        "content": chunk.get("content", ""),
                        "accumulated": chunk.get("accumulated", "")
                    }
                elif chunk.get("type") == "final":
                    data = chunk.get("data")
                    if data:
                        event_data = {
                            "type": "final",
                            "data": {
                                "thinking": data.thinking,
                                "rewritten_jd": data.rewritten_jd,
                                "key_changes": data.key_changes
                            }
                        }
                    else:
                        event_data = {"type": "error", "error": "No data in final chunk"}
                elif chunk.get("type") == "error":
                    event_data = {
                        "type": "error",
                        "error": chunk.get("error", "Unknown error"),
                        "raw_content": chunk.get("raw_content", "")
                    }
                else:
                    continue
                
                yield f"data: {json.dumps(event_data)}\n\n"
        except Exception as e:
            import traceback
            error_data = {
                "type": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/jd-ai/generate")
async def generate_jd(
    position: str = Form(...),
    experience_years: int = Form(...),
    required_skills: str = Form(...),
    salary_range: str = Form(...),
    job_type: str = Form(default="Full-time"),
    location: str = Form(default=""),
    benefits: str = Form(default=""),
    language: str = Form(default="en"),
    user_id: str = Depends(get_current_user_id),
    provider: Optional[str] = Header(default=None, alias="X-LLM-Provider")
):
    """Generate professional JD from requirements"""
    try:
        llm = get_llm_for_user(user_id, provider)
    except HTTPException as e:
        raise e
    
    jd_rewriter_agent = JDRewriterAgent(llm)
    
    # Build generation prompt
    lang_instruction = "Write in Vietnamese" if language == "vi" else "Write in English"
    
    prompt = f"""{lang_instruction}

Generate a professional job description for:
Position: {position}
Experience: {experience_years} years
Skills: {required_skills}
Salary: {salary_range}
Type: {job_type}
Location: {location or "Remote"}
Benefits: {benefits or "Competitive package"}

Include: Overview, Responsibilities, Requirements, Skills, Benefits, About Us
"""
    
    try:
        response = llm.invoke(prompt)
        generated_jd = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "success": True,
            "generated_jd": generated_jd,
            "inputs": {
                "position": position,
                "experience_years": experience_years,
                "skills": required_skills
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate JD: {str(e)}")
