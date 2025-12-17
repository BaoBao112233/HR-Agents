"""
Example: Extending other agents with streaming and structured outputs

This file shows how to apply the same streaming + structured output pattern
to other agents in the system (ScoreAgent, SummarizationAgent, etc.)
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from jd_assistants.agent.base import BaseAgent


# ============================================================================
# 1. Define Response Schemas
# ============================================================================

class CandidateScore(BaseModel):
    """Structured response for candidate scoring"""
    thinking: Optional[str] = Field(
        default=None,
        description="AI's reasoning process"
    )
    overall_score: int = Field(
        ge=0, le=100,
        description="Overall match score (0-100)"
    )
    technical_score: int = Field(
        ge=0, le=100,
        description="Technical skills match"
    )
    experience_score: int = Field(
        ge=0, le=100,
        description="Experience level match"
    )
    cultural_fit_score: int = Field(
        ge=0, le=100,
        description="Cultural fit assessment"
    )
    strengths: List[str] = Field(
        description="Candidate's key strengths"
    )
    weaknesses: List[str] = Field(
        description="Areas for improvement"
    )
    recommendation: str = Field(
        description="Hire/Maybe/Pass recommendation with reasoning"
    )


class CandidateSummary(BaseModel):
    """Structured response for candidate summarization"""
    thinking: Optional[str] = Field(
        default=None,
        description="AI's reasoning process"
    )
    summary: str = Field(
        description="Concise professional summary"
    )
    key_skills: List[str] = Field(
        description="Top skills identified"
    )
    highlights: List[str] = Field(
        description="Notable achievements or experience"
    )
    career_level: str = Field(
        description="Junior/Mid/Senior level assessment"
    )


# ============================================================================
# 2. Enhanced Score Agent
# ============================================================================

class EnhancedScoreAgent(BaseAgent):
    """Score agent with streaming and structured outputs"""
    
    def __init__(self, llm):
        system_prompt = """You are an expert technical recruiter. Analyze candidates 
        against job requirements and provide detailed scoring.
        
        Consider: technical skills, experience, cultural fit, growth potential.
        Be objective but also recognize potential and transferable skills.
        """
        super().__init__(name="Enhanced Score Agent", llm=llm, system_prompt=system_prompt)
    
    def score_candidate_structured(
        self, 
        candidate_info: dict, 
        jd_requirements: dict
    ) -> CandidateScore:
        """Score candidate with structured output"""
        input_text = f"""
        Evaluate this candidate against the job requirements:
        
        CANDIDATE:
        Name: {candidate_info.get('name')}
        Skills: {candidate_info.get('skills')}
        Experience: {candidate_info.get('bio')}
        
        JOB REQUIREMENTS:
        Title: {jd_requirements.get('title')}
        Required Skills: {jd_requirements.get('skills')}
        Description: {jd_requirements.get('description')}
        
        Provide:
        1. Your thinking process
        2. Scores for overall, technical, experience, cultural fit (0-100)
        3. List of strengths and weaknesses
        4. Final recommendation (Hire/Maybe/Pass)
        """
        return self.invoke_structured(input_text, CandidateScore)
    
    async def astream_score_candidate(
        self,
        candidate_info: dict,
        jd_requirements: dict
    ):
        """Stream candidate scoring"""
        input_text = f"""
        Evaluate this candidate in JSON format:
        
        CANDIDATE:
        Name: {candidate_info.get('name')}
        Skills: {candidate_info.get('skills')}
        Experience: {candidate_info.get('bio')}
        
        JOB REQUIREMENTS:
        Title: {jd_requirements.get('title')}
        Required Skills: {jd_requirements.get('skills')}
        
        Return JSON with: thinking, overall_score, technical_score, 
        experience_score, cultural_fit_score, strengths, weaknesses, recommendation
        """
        async for chunk in self.astream_structured(input_text, CandidateScore):
            yield chunk


# ============================================================================
# 3. Enhanced Summarization Agent
# ============================================================================

class EnhancedSummarizationAgent(BaseAgent):
    """Summarization agent with streaming and structured outputs"""
    
    def __init__(self, llm):
        system_prompt = """You are an expert at creating concise, 
        professional candidate summaries. Highlight key achievements and skills."""
        super().__init__(
            name="Enhanced Summarization Agent", 
            llm=llm, 
            system_prompt=system_prompt
        )
    
    def summarize_structured(self, candidate_data: dict) -> CandidateSummary:
        """Create structured candidate summary"""
        input_text = f"""
        Create a professional summary for this candidate:
        
        Name: {candidate_data.get('name')}
        Education: {candidate_data.get('education')}
        Work Experience: {candidate_data.get('work_experience')}
        Skills: {candidate_data.get('skills')}
        
        Provide:
        1. Your thinking process
        2. Concise professional summary (2-3 sentences)
        3. List of key skills
        4. Notable highlights
        5. Career level assessment
        """
        return self.invoke_structured(input_text, CandidateSummary)
    
    async def astream_summarize(self, candidate_data: dict):
        """Stream candidate summarization"""
        input_text = f"""
        Create summary in JSON format for:
        
        Name: {candidate_data.get('name')}
        Education: {candidate_data.get('education')}
        Work Experience: {candidate_data.get('work_experience')}
        Skills: {candidate_data.get('skills')}
        
        Return JSON with: thinking, summary, key_skills, highlights, career_level
        """
        async for chunk in self.astream_structured(input_text, CandidateSummary):
            yield chunk


# ============================================================================
# 4. Usage Examples
# ============================================================================

async def example_usage():
    """Example of how to use enhanced agents"""
    from jd_assistants.inference.groq import ChatGroq
    import os
    
    llm = ChatGroq(
        model='llama-3.3-70b-versatile',
        api_key=os.getenv('GROQ_API_KEY'),
        temperature=0
    )
    
    # Example 1: Score candidate with streaming
    score_agent = EnhancedScoreAgent(llm)
    
    candidate = {
        'name': 'John Doe',
        'skills': 'Python, React, Docker',
        'bio': '5 years of full-stack development experience'
    }
    
    jd = {
        'title': 'Senior Full-Stack Developer',
        'skills': 'Python, React, AWS',
        'description': 'Build scalable web applications'
    }
    
    print("Streaming candidate scoring...")
    async for chunk in score_agent.astream_score_candidate(candidate, jd):
        if chunk["type"] == "progress":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "final":
            result = chunk["data"]
            print(f"\n\nFinal Score: {result.overall_score}/100")
            print(f"Recommendation: {result.recommendation}")
    
    # Example 2: Summarize candidate without streaming
    summary_agent = EnhancedSummarizationAgent(llm)
    
    candidate_data = {
        'name': 'Jane Smith',
        'education': 'BS Computer Science, MIT',
        'work_experience': 'Senior Engineer at Google, 3 years',
        'skills': 'Python, Kubernetes, Machine Learning'
    }
    
    print("\n\nGenerating structured summary...")
    summary = summary_agent.summarize_structured(candidate_data)
    print(f"Summary: {summary.summary}")
    print(f"Career Level: {summary.career_level}")
    print(f"Key Skills: {', '.join(summary.key_skills)}")


# ============================================================================
# 5. API Endpoint Example
# ============================================================================

"""
Add to recruitment.py:

@router.post("/candidates/score-stream")
async def score_candidate_stream(
    candidate_id: str = Form(...),
    jd_id: int = Form(...),
    session: AsyncSession = Depends(get_session)
):
    '''Stream candidate scoring with thinking process'''
    candidate = await get_candidate_by_id(session, candidate_id)
    jd = await get_jd_by_id(session, jd_id)
    
    if not candidate or not jd:
        raise HTTPException(status_code=404, detail="Not found")
    
    async def event_generator():
        candidate_info = {
            'name': candidate.name,
            'skills': candidate.skills,
            'bio': candidate.bio
        }
        jd_info = {
            'title': jd.title,
            'skills': jd.skills,
            'description': jd.description
        }
        
        async for chunk in score_agent.astream_score_candidate(candidate_info, jd_info):
            if chunk["type"] == "progress":
                yield f"data: {json.dumps({'type': 'thinking', 'content': chunk['content']})}\n\n"
            elif chunk["type"] == "final":
                data = chunk["data"]
                yield f"data: {json.dumps({'type': 'final', 'data': data.dict()})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
"""


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
