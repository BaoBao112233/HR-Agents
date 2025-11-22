from jd_assistants.agent.base import BaseAgent

class SummarizationAgent(BaseAgent):
    def __init__(self, llm):
        system_prompt = """You are an expert HR assistant. Your task is to summarize the candidate's profile based on the extracted information.
        Create a comprehensive bio that highlights their key qualifications, experience, and skills.
        """
        super().__init__(name="Summarization Agent", llm=llm, system_prompt=system_prompt)

    def process(self, candidate_info: dict):
        input_text = f"""
        Name: {candidate_info.get('name')}
        Education: {candidate_info.get('education')}
        Work Experience: {candidate_info.get('work_experience')}
        Skills: {candidate_info.get('skills')}
        """
        return self.invoke(f"Summarize this candidate profile:\n{input_text}")
