from langchain_groq import ChatGroq as LangchainChatGroq
from langchain_core.messages import AIMessage
import json as json_lib

class ChatGroq(LangchainChatGroq):
    def __init__(self, model: str, api_key: str, temperature: float = 0, base_url: str = None):
        super().__init__(model_name=model, groq_api_key=api_key, temperature=temperature)

    def invoke(self, input, json: bool = False, **kwargs):
        if json:
            kwargs["response_format"] = {"type": "json_object"}
            res = super().invoke(input, **kwargs)
            try:
                if isinstance(res.content, str):
                    data = json_lib.loads(res.content)
                    res.content = data
            except:
                pass
            return res
        return super().invoke(input, **kwargs)


