# LiteLLM Multi-Agent System

A Python-based multi-agent system that uses LiteLLM for unified LLM access, supporting both OpenAI and Ollama backends. The system consists of two agents orchestrated via LangGraph: a Research Agent that gathers information on topics and a Content Generation Agent that creates articles based on the research.

## Features

- **Dynamic LLM Provider Switching**: Seamlessly switch between OpenAI and Ollama at runtime
- **Type-Safe Data Models**: All inputs/outputs validated with Pydantic
- **DAG-based Orchestration**: Agents connected via LangGraph for reliable workflow execution
- **CLI Interface**: Simple command-line tool for running the workflow
- **Configurable**: Environment-based configuration for API keys and settings

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Topic     │ --> │  Research Agent  │ --> │ Content Generation  │ --> Output
│   (input)   │     │   (LiteLLM)      │     │  Agent (LiteLLM)    │
└─────────────┘     └──────────────────┘     └─────────────────────┘
                           │                            │
                           └────────────────────────────┘
                                    LangGraph DAG
```

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- OpenAI API key (for OpenAI provider)
- Ollama installed locally (for Ollama provider)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd liteLLM
```

2. Install dependencies:
```bash
make setup
```

3. Configure environment variables:
```bash
# Edit the .env file with your API keys
# The setup command creates .env from .env.example
vi .env
```

### Environment Variables

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai  # Options: openai, ollama

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Ollama Configuration  
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Other Settings
LOG_LEVEL=INFO
```

## Usage

### Basic Usage

Run the workflow with a topic:
```bash
make run TOPIC="The impact of AI on education"
```

Or use the CLI directly:
```bash
poetry run python -m src.cli "The impact of AI on education"
```

### CLI Options

```bash
# Override LLM provider
python -m src.cli "Your topic" --provider ollama

# Save output to file
python -m src.cli "Your topic" --output results.json

# Enable verbose logging
python -m src.cli "Your topic" --verbose

# Get help
python -m src.cli --help
```

### Makefile Commands

```bash
make help        # Show available commands
make install     # Install dependencies
make setup       # Set up development environment
make run         # Run with default topic
make test        # Run tests
make clean       # Clean cache files
make format      # Format code with black
make lint        # Lint code with flake8
make check       # Run format and lint
```

## Project Structure

```
liteLLM/
├── pyproject.toml          # Poetry configuration
├── Makefile               # Build/run commands
├── .env.example           # Environment template
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic data models
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research.py    # Research agent
│   │   └── content.py     # Content generation agent
│   ├── workflow.py        # LangGraph orchestration
│   └── cli.py            # CLI interface
└── tests/
    ├── __init__.py
    └── test_workflow.py   # Test cases
```

## Example Output

```
🔍 Researching topic: The impact of AI on education
==================================================
Processing  [####################################]  100%

📚 Research Summary: The Impact of AI on Education
--------------------------------------------------
1. AI can personalize learning at scale
2. Automated grading saves time for educators
3. Virtual tutors provide 24/7 assistance
4. Data analytics help identify learning gaps
5. AI-powered tools enhance accessibility

📌 Sources:
- https://example.com/ai-education-study
- https://example.com/personalized-learning

📝 Article Summary:
--------------------------------------------------
AI is revolutionizing education through personalized learning experiences, 
automated administrative tasks, and enhanced accessibility for all students.

📄 Full Article:
==================================================
[Full article content here...]
```

## Development

### Running Tests

```bash
make test
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Run both
make check
```

### Adding Development Dependencies

```bash
poetry add --group dev <package-name>
```

## Troubleshooting

### OpenAI Provider Issues
- Ensure your `OPENAI_API_KEY` is set correctly in `.env`
- Check your API key has sufficient credits
- Verify the model name is correct (e.g., `gpt-4`, `gpt-3.5-turbo`)

### Ollama Provider Issues
- Ensure Ollama is running locally: `ollama serve`
- Verify the model is pulled: `ollama pull llama2`
- Check the base URL matches your Ollama instance

### General Issues
- Run with `--verbose` flag for detailed logging
- Check `.env` file exists and has correct values
- Ensure you're using Python 3.11+

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]