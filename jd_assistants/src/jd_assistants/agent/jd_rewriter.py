from jd_assistants.agent.base import BaseAgent
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
        
        Output your suggestions in JSON format:
        {
            "improvements": [
                {"section": "section_name", "original": "original text", "improved": "improved text", "reason": "why this is better"}
            ],
            "overall_score": int (0-100),
            "key_recommendations": ["recommendation1", "recommendation2"]
        }
        """
        super().__init__(name="JD Rewriter Agent", llm=llm, system_prompt=system_prompt)

    def analyze_jd(self, jd_text: str):
        """Analyze a job description and provide improvement suggestions"""
        input_text = f"""
        Analyze this job description and provide improvement suggestions:
        
        {jd_text}
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

    def rewrite_jd(self, jd_text: str, focus_areas: list = None):
        """Rewrite the entire JD with improvements"""
        focus = ", ".join(focus_areas) if focus_areas else "overall quality"
        input_text = f"""
        Rewrite this job description focusing on {focus}:
        
        {jd_text}
        
        Provide the complete rewritten JD in a clear, professional format.
        """
        return self.invoke(input_text)

    def improve_section(self, section_name: str, section_text: str):
        """Improve a specific section of the JD"""
        input_text = f"""
        Improve this {section_name} section of a job description:
        
        {section_text}
        
        Make it more engaging and clear.
        """
        return self.invoke(input_text)
