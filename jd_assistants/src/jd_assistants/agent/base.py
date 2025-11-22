from jd_assistants.inference import BaseInference
from langchain_core.messages import SystemMessage, HumanMessage

class BaseAgent:
    def __init__(self, name: str, llm: BaseInference, system_prompt: str = ""):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt

    def invoke(self, input_message: str, **kwargs):
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        response = self.llm.invoke(messages, **kwargs)
        return response.content
