"""
JD Analysis Agent - separate from JD Rewriter
Analyzes and evaluates job descriptions
"""
from jd_assistants.agent.base import BaseAgent
from jd_assistants.agent.response_schemas import JDAnalysisResponse
import json


class JDAnalysisAgent(BaseAgent):
    """Agent for analyzing and evaluating job descriptions"""
    
    def __init__(self, llm):
        system_prompt = """You are an expert HR and recruitment specialist focused on analyzing and evaluating job descriptions.

Your task is to:
1. Evaluate the quality and effectiveness of job descriptions
2. Identify strengths and weaknesses
3. Provide actionable recommendations for improvement
4. Score the overall quality

When analyzing a JD, focus on:
- Clarity and conciseness
- Inclusive language and bias-free content
- Realistic requirements and expectations
- Clear description of responsibilities
- Attraction factors (benefits, culture, growth)
- Proper structure and formatting
- Keyword optimization for job boards
- Legal compliance and best practices

IMPORTANT: Always provide your response in valid JSON format following the exact schema provided.
For models that support it, include a "thinking" field with your internal reasoning process.
"""
        super().__init__(name="JD Analysis Agent", llm=llm, system_prompt=system_prompt)
    
    def analyze(self, jd_text: str, language: str = "en") -> dict:
        """Analyze a job description and return analysis"""
        lang_instruction = ""
        if language == "vi":
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in Vietnamese (Tiếng Việt).\n\n"
        else:
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in English.\n\n"
        
        input_text = f"""{lang_instruction}
        Analyze and evaluate this job description:
        
        {jd_text}
        
        Provide a comprehensive analysis in JSON format with:
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
    
    def analyze_structured(self, jd_text: str, language: str = "en") -> JDAnalysisResponse:
        """Analyze JD with structured output"""
        lang_instruction = ""
        if language == "vi":
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in Vietnamese (Tiếng Việt).\n\n"
        else:
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in English.\n\n"
        
        input_text = f"""{lang_instruction}
        Analyze and evaluate this job description:
        
        {jd_text}
        
        Provide:
        1. Your internal reasoning in the thinking field
        2. An overall quality score (0-100)
        3. Key recommendations for improvement
        4. Specific improvements by section
        """
        
        return self.invoke_structured(input_text, JDAnalysisResponse)
    
    async def astream_analyze(self, jd_text: str, language: str = "en"):
        """Async stream analysis with structured output"""
        lang_instruction = ""
        if language == "vi":
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in Vietnamese (Tiếng Việt). All analysis, thinking, recommendations, and improvements must be in Vietnamese.\n\n"
        else:
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in English.\n\n"
        
        input_text = f"""{lang_instruction}
        Analyze and evaluate this job description.
        
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
    
    def quick_score(self, jd_text: str) -> dict:
        """Quick scoring without detailed analysis"""
        input_text = f"""
        Provide a quick quality score (0-100) for this job description:
        
        {jd_text}
        
        Return JSON with:
        {{
            "score": <integer 0-100>,
            "summary": "<brief 1-sentence assessment>"
        }}
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
    
    def compare_jds(self, jd1: str, jd2: str, language: str = "en") -> dict:
        """Compare two job descriptions"""
        lang_instruction = ""
        if language == "vi":
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in Vietnamese (Tiếng Việt).\n\n"
        else:
            lang_instruction = "\n\nIMPORTANT: Write the ENTIRE response in English.\n\n"
        
        input_text = f"""{lang_instruction}
        Compare these two job descriptions and determine which one is better:
        
        JD 1:
        {jd1}
        
        JD 2:
        {jd2}
        
        Return JSON with:
        {{
            "winner": "jd1" or "jd2",
            "score_jd1": <integer 0-100>,
            "score_jd2": <integer 0-100>,
            "comparison": "<detailed comparison>",
            "key_differences": ["difference 1", "difference 2", ...]
        }}
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
