import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Config(BaseModel):
    llm_provider: str = Field(default="openai", description="LLM provider: openai, ollama, anthropic, gemini, etc.")
    openai_api_key: Optional[str] = Field(default=None)
    openai_model: str = Field(default="gpt-4")
    anthropic_api_key: Optional[str] = Field(default=None)
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022")
    gemini_api_key: Optional[str] = Field(default=None)
    gemini_model: str = Field(default="gemini-1.5-pro")
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama2")
    log_level: str = Field(default="INFO")

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "openai").lower(),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama2"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    def get_litellm_model(self) -> str:
        if self.llm_provider == "openai":
            return self.openai_model
        elif self.llm_provider == "anthropic":
            return self.anthropic_model
        elif self.llm_provider == "gemini":
            return f"gemini/{self.gemini_model}"
        elif self.llm_provider == "ollama":
            return f"ollama/{self.ollama_model}"
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def get_litellm_kwargs(self) -> dict:
        kwargs = {}
        if self.llm_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            kwargs["api_key"] = self.openai_api_key
        elif self.llm_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider")
            kwargs["api_key"] = self.anthropic_api_key
        elif self.llm_provider == "gemini":
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is required for Gemini provider")
            kwargs["api_key"] = self.gemini_api_key
        elif self.llm_provider == "ollama":
            kwargs["api_base"] = self.ollama_base_url
        return kwargs