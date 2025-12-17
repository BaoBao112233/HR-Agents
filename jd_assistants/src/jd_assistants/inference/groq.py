from langchain_groq import ChatGroq as LangchainChatGroq
from langchain_core.messages import AIMessage
import json as json_lib
from typing import AsyncIterator, Iterator
from pydantic import BaseModel


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
    
    def stream(self, input, **kwargs):
        """Stream response tokens"""
        return super().stream(input, **kwargs)
    
    async def astream(self, input, **kwargs):
        """Async stream response tokens"""
        async for chunk in super().astream(input, **kwargs):
            yield chunk
    
    def stream_structured(self, input, schema: type[BaseModel], **kwargs):
        """Stream with structured output"""
        # Use with_structured_output for final parsing
        structured_llm = self.with_structured_output(schema, include_raw=False)
        return structured_llm.stream(input, **kwargs)
    
    async def astream_structured(self, input, schema: type[BaseModel], **kwargs):
        """Async stream with structured output"""
        structured_llm = self.with_structured_output(schema, include_raw=False)
        async for chunk in structured_llm.astream(input, **kwargs):
            yield chunk


