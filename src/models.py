from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchInput(BaseModel):
    topic: str = Field(..., description="The topic to research")


class ResearchOutput(BaseModel):
    title: str = Field(..., description="Title of the research")
    summary_points: List[str] = Field(..., description="Key points from the research")
    sources: List[str] = Field(default_factory=list, description="Sources referenced")


class ContentInput(BaseModel):
    research_output: ResearchOutput = Field(..., description="Research output to generate content from")


class ContentOutput(BaseModel):
    article: str = Field(..., description="Generated article content")
    summary: str = Field(..., description="Brief summary of the article")


class WorkflowState(BaseModel):
    topic: str = Field(..., description="Original topic")
    research_output: Optional[ResearchOutput] = None
    content_output: Optional[ContentOutput] = None
    error: Optional[str] = None