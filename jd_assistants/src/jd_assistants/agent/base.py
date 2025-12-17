from jd_assistants.inference import BaseInference
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import Optional, Iterator, AsyncIterator
import json


class BaseAgent:
    def __init__(self, name: str, llm: BaseInference, system_prompt: str = ""):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt

    def invoke(self, input_message: str, **kwargs):
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        response = self.llm.invoke(messages, **kwargs)
        return response.content
    
    def stream(self, input_message: str, **kwargs):
        """Stream response tokens"""
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        for chunk in self.llm.stream(messages, **kwargs):
            if hasattr(chunk, 'content'):
                yield chunk.content
            else:
                yield chunk
    
    async def astream(self, input_message: str, **kwargs):
        """Async stream response tokens"""
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        async for chunk in self.llm.astream(messages, **kwargs):
            if hasattr(chunk, 'content'):
                yield chunk.content
            else:
                yield chunk
    
    def invoke_structured(self, input_message: str, schema: type[BaseModel], **kwargs):
        """Invoke with structured output"""
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        structured_llm = self.llm.with_structured_output(schema, include_raw=False)
        response = structured_llm.invoke(messages, **kwargs)
        return response
    
    def stream_structured(self, input_message: str, schema: type[BaseModel], **kwargs):
        """Stream with structured output - yields partial structured responses"""
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        
        # For streaming structured outputs, we need to accumulate and parse
        accumulated_content = ""
        for chunk in self.llm.stream(messages, **kwargs):
            if hasattr(chunk, 'content') and chunk.content:
                accumulated_content += chunk.content
                # Yield progress updates
                yield {"type": "progress", "content": chunk.content, "accumulated": accumulated_content}
        
        # Final structured parse
        try:
            # Try to parse as JSON first
            data = json.loads(accumulated_content)
            structured_response = schema.model_validate(data)
            yield {"type": "final", "data": structured_response}
        except Exception as e:
            # If parsing fails, return raw content
            yield {"type": "error", "error": str(e), "raw_content": accumulated_content}
    
    async def astream_structured(self, input_message: str, schema: type[BaseModel], **kwargs):
        """Async stream with structured output"""
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=input_message)]
        
        # Force JSON mode if not already set
        if 'response_format' not in kwargs:
            kwargs['response_format'] = {"type": "json_object"}
        
        accumulated_content = ""
        async for chunk in self.llm.astream(messages, **kwargs):
            if hasattr(chunk, 'content') and chunk.content:
                accumulated_content += chunk.content
                yield {"type": "progress", "content": chunk.content, "accumulated": accumulated_content}
        
        # Final structured parse
        try:
            # Clean up any markdown code blocks or extra whitespace
            cleaned = accumulated_content.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            data = json.loads(cleaned)
            structured_response = schema.model_validate(data)
            yield {"type": "final", "data": structured_response}
        except json.JSONDecodeError as e:
            yield {"type": "error", "error": f"JSON parse error: {str(e)}", "raw_content": accumulated_content}
        except Exception as e:
            yield {"type": "error", "error": f"Validation error: {str(e)}", "raw_content": accumulated_content}

