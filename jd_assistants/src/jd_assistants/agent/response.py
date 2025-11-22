from jd_assistants.agent.base import BaseAgent

class ResponseAgent(BaseAgent):
    def __init__(self, llm):
        system_prompt = """You are an expert HR Assistant. Your task is to write an email to a candidate regarding their application.
        If the candidate is selected (proceed_with_candidate=True), write a congratulatory email inviting them for an interview.
        If not selected, write a polite rejection email.
        """
        super().__init__(name="Response Agent", llm=llm, system_prompt=system_prompt)

    def process(self, candidate, proceed_with_candidate: bool):
        input_text = f"""
        Candidate Name: {candidate.name}
        Bio: {candidate.bio}
        Selected: {proceed_with_candidate}
        """
        return self.invoke(f"Write an email for this candidate:\n{input_text}")
