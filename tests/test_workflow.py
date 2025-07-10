import pytest
from unittest.mock import Mock, patch
from src.models import ResearchInput, ResearchOutput, ContentInput, ContentOutput, WorkflowState
from src.config import Config
from src.agents.research import ResearchAgent
from src.agents.content import ContentGenerationAgent


class TestModels:
    def test_research_input(self):
        input_data = ResearchInput(topic="AI in healthcare")
        assert input_data.topic == "AI in healthcare"
    
    def test_research_output(self):
        output = ResearchOutput(
            title="AI in Healthcare",
            summary_points=["Point 1", "Point 2"],
            sources=["Source 1"]
        )
        assert output.title == "AI in Healthcare"
        assert len(output.summary_points) == 2
        assert len(output.sources) == 1
    
    def test_content_output(self):
        output = ContentOutput(
            article="Article content",
            summary="Brief summary"
        )
        assert output.article == "Article content"
        assert output.summary == "Brief summary"


class TestConfig:
    def test_config_defaults(self):
        config = Config()
        assert config.llm_provider == "openai"
        assert config.openai_model == "gpt-4"
        assert config.ollama_model == "llama2"
    
    def test_get_litellm_model_openai(self):
        config = Config(llm_provider="openai", openai_model="gpt-3.5-turbo")
        assert config.get_litellm_model() == "gpt-3.5-turbo"
    
    def test_get_litellm_model_ollama(self):
        config = Config(llm_provider="ollama", ollama_model="mistral")
        assert config.get_litellm_model() == "ollama/mistral"
    
    def test_invalid_provider(self):
        config = Config(llm_provider="invalid")
        with pytest.raises(ValueError):
            config.get_litellm_model()


class TestAgents:
    @patch('src.agents.research.completion')
    def test_research_agent(self, mock_completion):
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"title": "Test Title", "summary_points": ["Point 1"], "sources": []}'))]
        mock_completion.return_value = mock_response
        
        config = Config(openai_api_key="test-key")
        agent = ResearchAgent(config)
        
        input_data = ResearchInput(topic="Test topic")
        result = agent.research(input_data)
        
        assert result.title == "Test Title"
        assert result.summary_points == ["Point 1"]
        assert result.sources == []
    
    @patch('src.agents.content.completion')
    def test_content_agent(self, mock_completion):
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"article": "Test article", "summary": "Test summary"}'))]
        mock_completion.return_value = mock_response
        
        config = Config(openai_api_key="test-key")
        agent = ContentGenerationAgent(config)
        
        research = ResearchOutput(
            title="Test",
            summary_points=["Point 1"],
            sources=[]
        )
        input_data = ContentInput(research_output=research)
        result = agent.generate_content(input_data)
        
        assert result.article == "Test article"
        assert result.summary == "Test summary"


class TestWorkflowIntegration:
    def test_workflow_state(self):
        state = WorkflowState(
            topic="Test topic",
            research_output=ResearchOutput(
                title="Test",
                summary_points=["Point 1"],
                sources=[]
            ),
            content_output=ContentOutput(
                article="Article",
                summary="Summary"
            ),
            error=None
        )
        
        assert state.topic == "Test topic"
        assert state.research_output.title == "Test"
        assert state.content_output.article == "Article"
        assert state.error is None