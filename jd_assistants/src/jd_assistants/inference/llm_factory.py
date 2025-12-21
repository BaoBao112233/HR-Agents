"""
Multi-LLM provider support: Groq, OpenRouter, Gemini, GPT
"""
from typing import Literal, Optional
from langchain_groq import ChatGroq as LangchainChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import json as json_lib
from pydantic import BaseModel


LLMProvider = Literal["groq", "openrouter", "gemini", "gpt", "openai"]


class BaseInference:
    """Base class for LLM inference"""
    
    def __init__(self, model: str, api_key: str, temperature: float = 0):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.client = None
    
    def invoke(self, input, json: bool = False, **kwargs):
        raise NotImplementedError
    
    def stream(self, input, **kwargs):
        raise NotImplementedError
    
    async def astream(self, input, **kwargs):
        raise NotImplementedError
    
    def with_structured_output(self, schema: type[BaseModel], **kwargs):
        raise NotImplementedError


class GroqInference(BaseInference):
    """Groq LLM client"""
    
    def __init__(self, model: str, api_key: str, temperature: float = 0):
        super().__init__(model, api_key, temperature)
        self.client = LangchainChatGroq(
            model_name=model,
            groq_api_key=api_key,
            temperature=temperature
        )
    
    def invoke(self, input, json: bool = False, **kwargs):
        if json:
            kwargs["response_format"] = {"type": "json_object"}
            res = self.client.invoke(input, **kwargs)
            try:
                if isinstance(res.content, str):
                    data = json_lib.loads(res.content)
                    res.content = data
            except:
                pass
            return res
        return self.client.invoke(input, **kwargs)
    
    def stream(self, input, **kwargs):
        return self.client.stream(input, **kwargs)
    
    async def astream(self, input, **kwargs):
        async for chunk in self.client.astream(input, **kwargs):
            yield chunk
    
    def with_structured_output(self, schema: type[BaseModel], **kwargs):
        return self.client.with_structured_output(schema, **kwargs)


class OpenRouterInference(BaseInference):
    """OpenRouter LLM client (using OpenAI-compatible API)"""
    
    def __init__(self, model: str, api_key: str, temperature: float = 0):
        super().__init__(model, api_key, temperature)
        self.client = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=temperature
        )
    
    def invoke(self, input, json: bool = False, **kwargs):
        if json:
            kwargs["response_format"] = {"type": "json_object"}
            res = self.client.invoke(input, **kwargs)
            try:
                if isinstance(res.content, str):
                    data = json_lib.loads(res.content)
                    res.content = data
            except:
                pass
            return res
        return self.client.invoke(input, **kwargs)
    
    def stream(self, input, **kwargs):
        return self.client.stream(input, **kwargs)
    
    async def astream(self, input, **kwargs):
        async for chunk in self.client.astream(input, **kwargs):
            yield chunk
    
    def with_structured_output(self, schema: type[BaseModel], **kwargs):
        return self.client.with_structured_output(schema, **kwargs)


class GeminiInference(BaseInference):
    """Google Gemini LLM client"""
    
    def __init__(self, model: str, api_key: str, temperature: float = 0):
        super().__init__(model, api_key, temperature)
        self.client = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature
        )
    
    def invoke(self, input, json: bool = False, **kwargs):
        if json:
            # Gemini uses different JSON mode configuration
            res = self.client.invoke(input, **kwargs)
            try:
                if isinstance(res.content, str):
                    # Try to extract JSON from response
                    content = res.content.strip()
                    if content.startswith('```json'):
                        content = content[7:]
                    if content.startswith('```'):
                        content = content[3:]
                    if content.endswith('```'):
                        content = content[:-3]
                    data = json_lib.loads(content.strip())
                    res.content = data
            except:
                pass
            return res
        return self.client.invoke(input, **kwargs)
    
    def stream(self, input, **kwargs):
        return self.client.stream(input, **kwargs)
    
    async def astream(self, input, **kwargs):
        async for chunk in self.client.astream(input, **kwargs):
            yield chunk
    
    def with_structured_output(self, schema: type[BaseModel], **kwargs):
        return self.client.with_structured_output(schema, **kwargs)


class OpenAIInference(BaseInference):
    """OpenAI GPT LLM client"""
    
    def __init__(self, model: str, api_key: str, temperature: float = 0):
        super().__init__(model, api_key, temperature)
        self.client = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            temperature=temperature
        )
    
    def invoke(self, input, json: bool = False, **kwargs):
        if json:
            kwargs["response_format"] = {"type": "json_object"}
            res = self.client.invoke(input, **kwargs)
            try:
                if isinstance(res.content, str):
                    data = json_lib.loads(res.content)
                    res.content = data
            except:
                pass
            return res
        return self.client.invoke(input, **kwargs)
    
    def stream(self, input, **kwargs):
        return self.client.stream(input, **kwargs)
    
    async def astream(self, input, **kwargs):
        async for chunk in self.client.astream(input, **kwargs):
            yield chunk
    
    def with_structured_output(self, schema: type[BaseModel], **kwargs):
        return self.client.with_structured_output(schema, **kwargs)


# LLM Factory
def create_llm(
    provider: LLMProvider,
    model: str,
    api_key: str,
    temperature: float = 0
) -> BaseInference:
    """
    Create LLM client based on provider
    
    Args:
        provider: One of "groq", "openrouter", "gemini", "gpt", "openai"
        model: Model name (e.g., "llama-3.3-70b-versatile", "gpt-4o", "gemini-pro")
        api_key: API key for the provider
        temperature: Temperature for generation
    
    Returns:
        BaseInference instance
    """
    provider = provider.lower()
    
    if provider == "groq":
        return GroqInference(model, api_key, temperature)
    elif provider == "openrouter":
        return OpenRouterInference(model, api_key, temperature)
    elif provider == "gemini":
        return GeminiInference(model, api_key, temperature)
    elif provider in ["gpt", "openai"]:
        return OpenAIInference(model, api_key, temperature)
    else:
        raise ValueError(f"Unsupported provider: {provider}. Must be one of: groq, openrouter, gemini, gpt, openai")


# Default models for each provider
DEFAULT_MODELS = {
    "groq": "llama-3.3-70b-versatile",
    "openrouter": "anthropic/claude-3.5-sonnet",
    "gemini": "gemini-1.5-pro",
    "gpt": "gpt-4o",
    "openai": "gpt-4o"
}


def get_default_model(provider: LLMProvider) -> str:
    """Get default model for a provider"""
    return DEFAULT_MODELS.get(provider.lower(), "gpt-4o")
