"""
Pydantic schemas for structured outputs with thinking support
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ImprovementSuggestion(BaseModel):
    """Single improvement suggestion for JD"""
    section: str = Field(description="The section name being improved")
    original: str = Field(description="Original text from the section")
    improved: str = Field(description="Improved version of the text")
    reason: str = Field(description="Explanation for why this is better")


class JDAnalysisResponse(BaseModel):
    """Structured response for JD analysis with thinking"""
    thinking: Optional[str] = Field(
        default=None,
        description="Internal reasoning process (only for models that support it)"
    )
    overall_score: int = Field(
        ge=0, le=100,
        description="Overall quality score of the JD"
    )
    key_recommendations: List[str] = Field(
        description="List of key recommendations for improvement"
    )
    improvements: List[ImprovementSuggestion] = Field(
        description="Detailed improvement suggestions by section"
    )


class JDRewriteResponse(BaseModel):
    """Structured response for JD rewriting with thinking"""
    thinking: Optional[str] = Field(
        default=None,
        description="Internal reasoning process (only for models that support it)"
    )
    rewritten_jd: str = Field(
        description="Complete rewritten job description"
    )
    key_changes: List[str] = Field(
        description="Summary of major changes made"
    )


class JDGenerateResponse(BaseModel):
    """Structured response for JD generation with thinking"""
    thinking: Optional[str] = Field(
        default=None,
        description="Internal reasoning process (only for models that support it)"
    )
    job_description: str = Field(
        description="Generated job description"
    )
    title: str = Field(
        description="Job title"
    )
    key_highlights: List[str] = Field(
        description="Key highlights of the position"
    )


class SalaryAssessmentResponse(BaseModel):
    """Structured response for salary assessment"""
    thinking: Optional[str] = Field(
        default=None,
        description="Internal reasoning process"
    )
    recommended_range: str = Field(
        description="Recommended salary range"
    )
    market_analysis: str = Field(
        description="Analysis of market conditions"
    )
    competitiveness_score: int = Field(
        ge=0, le=100,
        description="How competitive the salary is"
    )
    suggestions: List[str] = Field(
        description="Suggestions for improving compensation package"
    )
