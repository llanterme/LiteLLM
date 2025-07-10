import logging
from typing import Dict, Any
import instructor
from litellm import completion
from ..models import ResearchInput, ResearchOutput
from ..config import Config

logger = logging.getLogger(__name__)


class ResearchAgent:
    def __init__(self, config: Config):
        self.config = config
        self.model = config.get_litellm_model()
        self.llm_kwargs = config.get_litellm_kwargs()

    def _create_prompt(self, topic: str) -> str:
        return f"""You are a research assistant. Your task is to research the topic: "{topic}"

Please provide a comprehensive research summary with:
1. A clear title for the research
2. 5-7 key summary points about the topic  
3. 2-3 credible sources (if applicable)

Ensure your research is factual, balanced, and informative."""

    def research(self, input_data: ResearchInput) -> ResearchOutput:
        try:
            logger.info(f"Researching topic: {input_data.topic}")
            
            prompt = self._create_prompt(input_data.topic)
            
            # Create instructor client from litellm completion
            client = instructor.from_litellm(completion)
            
            # Get structured output directly as ResearchOutput with retries
            research_output = client.chat.completions.create(
                model=self.model,
                response_model=ResearchOutput,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_retries=3,
                **self.llm_kwargs
            )
            
            logger.info(f"Research completed: {research_output.title}")
            return research_output
            
        except Exception as e:
            logger.error(f"Error in research agent: {str(e)}")
            raise

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        input_data = ResearchInput(topic=state["topic"])
        research_output = self.research(input_data)
        state["research_output"] = research_output
        return state