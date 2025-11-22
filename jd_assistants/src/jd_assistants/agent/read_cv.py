from jd_assistants.agent.base import BaseAgent
from jd_assistants.tools.read_pdf_tool import convert_response_to_json_string
import json

class ReadCVAgent(BaseAgent):
    def __init__(self, llm):
        system_prompt = """You are an expert in reading and extracting information from CVs/Resumes.
        Your task is to extract the following information from the provided CV content:
        - personal_info (name, email, phone, job_title, dob, address)
        - education (university, major, start_date, end_date, descriptions)
        - work_experience (company, position, start_date, end_date, descriptions)
        - skills (name, levels, descriptions)
        
        Output the result in a valid JSON format with keys in snake_case.

        """
        super().__init__(name="Read CV Agent", llm=llm, system_prompt=system_prompt)

    def process(self, pdf_content: str, file_name: str):
        response = self.invoke(f"Extract information from this CV content:\n{pdf_content}", json=True)
        # Assuming response is already a dict if json=True in our wrapper, 
        # but the original logic used convert_response_to_json_string which handles markdown code blocks.
        # Let's check if our wrapper returns dict or str.
        # The wrapper returns dict if json=True and the content is valid json.
        
        if isinstance(response, dict):
             # We might need to clean it using the existing utility
             from jd_assistants.tools.read_pdf_tool import clean_data
             return clean_data(response)
        
        # If it's a string (maybe the wrapper failed to parse or returned raw string), use the utility
        return convert_response_to_json_string(str(response), file_name)
