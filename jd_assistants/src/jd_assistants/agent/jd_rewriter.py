from jd_assistants.agent.base import BaseAgent
from jd_assistants.agent.response_schemas import (
    JDAnalysisResponse, 
    JDRewriteResponse,
    JDGenerateResponse
)
import json


class JDRewriterAgent(BaseAgent):
    def __init__(self, llm):
        system_prompt = """You are an expert HR and recruitment specialist. Your task is to analyze and improve job descriptions to make them more attractive to candidates while maintaining accuracy.

        When analyzing a JD, focus on:
        1. Clarity and conciseness
        2. Highlighting benefits and growth opportunities
        3. Using inclusive language
        4. Proper formatting and structure
        5. Emphasizing company culture and values
        
        IMPORTANT: Always provide your response in valid JSON format following the exact schema provided.
        For models that support it, include a "thinking" field with your internal reasoning process.
        """
        super().__init__(name="JD Rewriter Agent", llm=llm, system_prompt=system_prompt)

    def analyze_jd(self, jd_text: str):
        """Analyze a job description and provide improvement suggestions"""
        input_text = f"""
        Analyze this job description and provide improvement suggestions in JSON format:
        
        {jd_text}
        
        Return a JSON object with:
        - thinking (optional): Your reasoning process
        - overall_score: integer 0-100
        - key_recommendations: array of recommendation strings
        - improvements: array of objects with section, original, improved, reason
        """
        response = self.invoke(input_text, json=True)
        
        if isinstance(response, str):
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
            except:
                pass
                
        return response

    def analyze_jd_structured(self, jd_text: str) -> JDAnalysisResponse:
        """Analyze JD with structured output"""
        input_text = f"""
        Analyze this job description and provide improvement suggestions:
        
        {jd_text}
        
        Provide:
        1. Your internal reasoning in the thinking field
        2. An overall quality score (0-100)
        3. Key recommendations for improvement
        4. Specific improvements by section
        """
        return self.invoke_structured(input_text, JDAnalysisResponse)
    
    async def astream_analyze_jd(self, jd_text: str, language: str = "en"):
        """Async stream analysis with structured output"""
        # Language instruction
        lang_instruction = ""
        if language == "vi":
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in Vietnamese (Tiếng Việt). All analysis, thinking, recommendations, and improvements must be in Vietnamese.\n\n"
        else:
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in English.\n\n"
        
        input_text = f"""{lang_instruction}
        Analyze this job description and provide improvement suggestions.
        
        JOB DESCRIPTION:
        {jd_text}
        
        You MUST respond with a valid JSON object following this exact structure:
        {{
            "thinking": "Your detailed reasoning process here",
            "overall_score": 75,
            "key_recommendations": ["recommendation 1", "recommendation 2"],
            "improvements": [
                {{
                    "section": "Section name",
                    "original": "Original text",
                    "improved": "Improved text",
                    "reason": "Why this is better"
                }}
            ]
        }}
        
        IMPORTANT: Return ONLY valid JSON, no other text before or after.
        """
        async for chunk in self.astream_structured(input_text, JDAnalysisResponse):
            yield chunk

    def rewrite_jd(self, jd_text: str, focus_areas: list = None):
        """Rewrite the entire JD with improvements"""
        focus = ", ".join(focus_areas) if focus_areas else "overall quality"
        input_text = f"""
        Rewrite this job description focusing on {focus}:
        
        {jd_text}
        
        Provide the complete rewritten JD in a clear, professional format.
        """
        return self.invoke(input_text)

    def rewrite_jd_structured(self, jd_text: str, focus_areas: list = None) -> JDRewriteResponse:
        """Rewrite JD with structured output"""
        focus = ", ".join(focus_areas) if focus_areas else "overall quality"
        input_text = f"""
        Rewrite this job description focusing on {focus}:
        
        {jd_text}
        
        Provide:
        1. Your thinking process
        2. The complete rewritten job description
        3. A list of key changes made
        """
        return self.invoke_structured(input_text, JDRewriteResponse)
    
    async def astream_rewrite_jd(self, jd_text: str, focus_areas: list = None, language: str = "en"):
        """Async stream rewrite with structured output"""
        focus = ", ".join(focus_areas) if focus_areas else "overall quality"
        
        # Language instruction
        lang_instruction = ""
        if language == "vi":
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE rewritten job description in Vietnamese (Tiếng Việt). All content, thinking, and key changes must be in Vietnamese.\n\n"
        else:
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE rewritten job description in English.\n\n"
        
        input_text = f"""{lang_instruction}
        Rewrite this job description focusing on {focus}.
        
        ORIGINAL JD:
        {jd_text}
        
        You MUST respond with a valid JSON object following this exact structure:
        {{
            "thinking": "Your reasoning about improvements",
            "rewritten_jd": "Complete rewritten job description here",
            "key_changes": ["change 1", "change 2", "change 3"]
        }}
        
        IMPORTANT: Return ONLY valid JSON, no other text before or after.
        """
        async for chunk in self.astream_structured(input_text, JDRewriteResponse):
            yield chunk

    def improve_section(self, section_name: str, section_text: str):
        """Improve a specific section of the JD"""
        input_text = f"""
        Improve this {section_name} section of a job description:
        
        {section_text}
        
        Make it more engaging and clear.
        """
        return self.invoke(input_text)
    
    def generate_jd(self, requirements: dict) -> JDGenerateResponse:
        """Generate a complete JD from requirements"""
        input_text = f"""
        Generate a complete job description based on these requirements:
        
        Position: {requirements.get('position')}
        Experience: {requirements.get('experience_years')} years
        Skills: {requirements.get('required_skills')}
        Salary Range: {requirements.get('salary_range')}
        Job Type: {requirements.get('job_type', 'Full-time')}
        Location: {requirements.get('location', 'Not specified')}
        
        Provide:
        1. Your thinking process
        2. A complete, professional job description
        3. An appropriate job title
        4. Key highlights of the position
        """
        return self.invoke_structured(input_text, JDGenerateResponse)
    
    async def astream_generate_jd(self, requirements: dict):
        """Async stream JD generation"""
        input_text = f"""
        Generate a complete job description in JSON format:
        
        Position: {requirements.get('position')}
        Experience: {requirements.get('experience_years')} years
        Skills: {requirements.get('required_skills')}
        Salary Range: {requirements.get('salary_range')}
        Job Type: {requirements.get('job_type', 'Full-time')}
        Location: {requirements.get('location', 'Not specified')}
        
        Return JSON with:
        - thinking: Your reasoning
        - job_description: Complete JD text
        - title: Job title
        - key_highlights: Array of highlights
        """
        async for chunk in self.astream_structured(input_text, JDGenerateResponse):
            yield chunk

