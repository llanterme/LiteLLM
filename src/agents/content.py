import logging
from typing import Dict, Any
import instructor
from litellm import completion
from ..models import ContentInput, ContentOutput, ResearchOutput
from ..config import Config

logger = logging.getLogger(__name__)


class ContentGenerationAgent:
    def __init__(self, config: Config):
        self.config = config
        self.model = config.get_litellm_model()
        self.llm_kwargs = config.get_litellm_kwargs()

    def _create_prompt(self, research: ResearchOutput) -> str:
        summary_points_str = "\n".join([f"- {point}" for point in research.summary_points])
        sources_str = "\n".join([f"- {source}" for source in research.sources]) if research.sources else "No sources provided"
        
        return f"""Based on the following research, write a comprehensive article.

Research Title: {research.title}

Key Points:
{summary_points_str}

Sources:
{sources_str}

Please write:
1. A well-structured article (500-800 words) that expands on these research points
2. A brief 2-3 sentence summary of the article

Make the article engaging, informative, and well-organized with clear sections."""

    def generate_content(self, input_data: ContentInput) -> ContentOutput:
        try:
            logger.info(f"Generating content for: {input_data.research_output.title}")
            
            prompt = self._create_prompt(input_data.research_output)
            
            # Create instructor client from litellm completion
            client = instructor.from_litellm(completion)
            
            # Get structured output directly as ContentOutput with retries
            content_output = client.chat.completions.create(
                model=self.model,
                response_model=ContentOutput,
                messages=[
                    {"role": "system", "content": "You are a skilled content writer who creates engaging, informative articles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000,
                max_retries=3,
                **self.llm_kwargs
            )
            
            logger.info("Content generation completed")
            return content_output
            
        except Exception as e:
            logger.error(f"Error in content generation agent: {str(e)}")
            raise

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if not state.get("research_output"):
            raise ValueError("Research output not found in state")
        
        input_data = ContentInput(research_output=state["research_output"])
        content_output = self.generate_content(input_data)
        state["content_output"] = content_output
        return state