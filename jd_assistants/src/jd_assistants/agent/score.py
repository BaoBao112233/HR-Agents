from jd_assistants.agent.base import BaseAgent
import json

class ScoreAgent(BaseAgent):
    def __init__(self, llm):
        system_prompt = """You are an expert HR Recruiter. Your task is to score a candidate based on their profile and the job description.
        Score from 0 to 100. Provide a reason for the score.
        
        Output JSON format:
        {
            "id": "candidate_id",
            "name": "candidate_name",
            "score": int,
            "reason": "explanation"
        }
        """
        super().__init__(name="Score Agent", llm=llm, system_prompt=system_prompt)

    def process(self, candidate, job_description, skills, additional_instructions=""):
        input_text = f"""
        Candidate ID: {candidate.id}
        Name: {candidate.name}
        Bio: {candidate.bio}
        
        Job Description:
        {job_description}
        
        Required Skills:
        {skills}
        
        Additional Instructions:
        {additional_instructions}
        """
        response = self.invoke(f"Score this candidate:\n{input_text}", json=True)
        if isinstance(response, str):
             # Fallback if wrapper didn't parse json
             try:
                 import re
                 json_match = re.search(r'\{.*\}', response, re.DOTALL)
                 if json_match:
                     return json.loads(json_match.group(0))
             except:
                 pass
        return response
