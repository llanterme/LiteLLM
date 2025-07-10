## 1. **Identify the Coding Goal and Context**

* **Goal:**
  Create a Python-based, multi-agent system using [LiteLLM](https://docs.litellm.ai/docs/) that can switch between multiple LLM backends (OpenAI, Anthropic, Gemini, Ollama, and 15+ others) seamlessly at runtime.

* **Agents:**

  * Research Agent: Gathers information on a topic.
  * Content Generation Agent: Writes content using the research agent’s findings.

* **Technologies/Frameworks:**

  * LiteLLM (for unified LLM API across 15+ providers)
  * Instructor (for robust structured outputs from any LLM)
  * Pydantic (for data models and validation)
  * LangGraph (for agent orchestration in DAG style)
  * Poetry (for dependency, packaging, virtualenv) - ALWAYS use virtual environments.

* **Environment:**

  * Python 3.11+
  
---

## 2. **Structure the Prompt Components**

### **Prompt for the Agentic Coding System**

````markdown
## Context

You are building a Python system for agentic orchestration using the following stack:

- [LiteLLM](https://docs.litellm.ai/docs/) for unified LLM access across 15+ providers. The system must allow dynamic switching between OpenAI, Anthropic, Gemini, Ollama, and other backends at runtime, ideally by configuration or environment variable.
- [Instructor](https://python.useinstructor.com/) for robust structured outputs from any LLM without manual JSON parsing.
- [LangGraph](https://github.com/langchain-ai/langgraph) for DAG-style agent orchestration.
- [Pydantic](https://docs.pydantic.dev/latest/) for all data models, ensuring type safety and validation.
- [Poetry](https://python-poetry.org/docs/) for dependency management, packaging, and virtualenv creation.

This system will contain two main agents:
1. **Research Agent:** Accepts a topic, researches it using the selected LLM, and outputs a structured research summary.
2. **Content Generation Agent:** Accepts the research summary and generates an article, essay, or content piece based on that information.


## Requirements

### Functional

- The system must enable easy switching between multiple LLM providers (OpenAI, Anthropic, Gemini, Ollama, etc.) ideally by config or environment variable.
- Research agent: Accepts a topic string; returns a Pydantic-typed research summary (with title, bullet points, sources if possible).
- Content generation agent: Accepts the research summary; returns Pydantic-typed content (article body, summary, etc.).
- Use LangGraph to orchestrate both agents in a directed acyclic graph where the research agent runs first, then passes its output to the content generation agent.
- Expose a CLI or simple script interface to run the workflow end-to-end with a given topic.

### Non-Functional

- Use Pydantic models for all agent inputs and outputs. 
- Use Poetry for dependency management and packaging (generate pyproject.toml). ALWAYS use virtual environments.
- Ensure clear error handling for invalid config, missing dependencies, or failed LLM calls.
- Modular, well-documented code.
- Create a Makefile for all comamands

---

## Workflow Guidance

1. **Environment Setup:**
    - Use Poetry to initialize project and manage dependencies.

2. **Configuration:**
    - Design a config system (.env) or use environment variables for backend selection and LLM API keys.

3. **Agent Implementation:**
    - Implement each agent as a class or function.
    - Use Instructor + Pydantic for robust structured outputs (NO manual JSON parsing).
    - Research agent uses LiteLLM + Instructor to get validated ResearchOutput.
    - Content generation agent uses LiteLLM + Instructor to get validated ContentOutput.

4. **Graph Construction:**
    - Use LangGraph to connect agents in a DAG, ensuring research agent runs before content generation.
    - Ensure proper data passing and type validation between agents.

5. **Execution Interface:**
    - Provide a simple CLI or script to accept a topic, execute the workflow, and display/return the final content.

6. **Testing and Validation:**
    - Include example topics and validate the workflow with test cases.

---

## Acceptance Criteria

- The system works with multiple LLM providers (OpenAI, Anthropic, Gemini, Ollama, etc.) and can be switched at runtime.
- Outputs are validated with Pydantic models.
- The DAG workflow correctly chains agents via LangGraph.
- The workflow can be run from the CLI.
- All code is managed via Poetry.

---

## Example Input/Output

**Input:** `"The impact of AI on education"`

**Research Agent Output (Pydantic Model):**
```python
{
  "title": "The Impact of AI on Education",
  "summary_points": [
    "AI can personalize learning at scale",
    "Automated grading saves time for educators",
    ...
  ],
  "sources": [
    "https://example.com/source1",
    ...
  ]
}
````

**Content Generation Agent Output (Pydantic Model):**

```python
{
  "article": "Artificial intelligence (AI) is transforming education by enabling personalized learning...",
  "summary": "AI revolutionizes education through personalization and automation."
}
```

---

## Notes

* Include all necessary import statements and config scaffolding.
* Document code and include inline comments explaining logic and workflow.
* Write a README.md with instructions for setup, configuration, and usage.


### **Explanation & Key Components**

- **Context:** Lays out environment, frameworks, and agentic approach.
- **Requirements:** Separates functional (what it must do) and non-functional (how it should do it) needs.
- **Workflow Guidance:** Step-by-step, clear tasks for the agent to follow—this is crucial for agentic systems.
- **Acceptance Criteria:** Ensures clarity on what constitutes "done."
- **Examples:** Provides data shape and expectations for I/O.

---

### **Assumptions**

- User will provide required LLM keys/configuration.
- LLMs (OpenAI, Anthropic, Gemini, Ollama, etc.) are accessible in the environment.
- LangGraph, LiteLLM, and Instructor are compatible and installable via Poetry.
- User is comfortable with command line.


## ✅ Implementation Status (COMPLETED)

This project has been **fully implemented** and is production-ready with the following features:

### **🚀 Core Features**
- ✅ **Multi-LLM Support**: OpenAI, Anthropic, Gemini, Ollama, and 15+ providers
- ✅ **Zero JSON Parsing**: Uses Instructor library for robust structured outputs
- ✅ **Type Safety**: Full Pydantic validation with automatic retries
- ✅ **DAG Orchestration**: LangGraph workflow with error handling
- ✅ **CLI Interface**: Easy-to-use command line with provider switching
- ✅ **Configuration**: Environment-based config with .env support

### **📁 Project Structure**
```
liteLLM/
├── src/
│   ├── agents/
│   │   ├── research.py     # Research Agent (Instructor + LiteLLM)
│   │   └── content.py      # Content Agent (Instructor + LiteLLM)
│   ├── config.py           # Multi-provider configuration
│   ├── models.py           # Pydantic data models
│   ├── workflow.py         # LangGraph DAG orchestration
│   └── cli.py              # CLI interface
├── tests/                  # Test suite
├── Makefile               # Build/run commands
├── .gitignore             # Security & cleanup
└── README.md              # Full documentation
```

### **🔧 Usage Examples**
```bash
# OpenAI
make run-openai TOPIC="AI trends"

# Anthropic Claude  
make run-anthropic TOPIC="AI trends"

# Local Ollama
make run-ollama TOPIC="AI trends"

# Direct CLI
python -m src.cli "AI trends" --provider anthropic
```

### **🎯 Key Innovations**
- **LLM Agnostic**: Switch providers with single environment variable
- **No Regex/JSON Parsing**: Instructor handles all structured output complexity
- **Production Ready**: Comprehensive error handling, retries, validation
- **Extensible**: Easy to add new LLM providers

---

##  General Principles

- **Clean Code:**  
  - Follow PEP 8 and The Zen of Python.  
  - Keep functions/classes small (≤ 50 lines). Single responsibility per function/class.  
  - Use descriptive names.  
  - Delete dead code; avoid commented-out code.  
  - Prioritize readability over cleverness.

- **Functional Style & Immutability:**  
  - Favor pure functions without side effects.  
  - Use immutable structures (tuples, `frozenset`) when data shouldn't change.  
  - Minimize global mutable state.

- **Structured Outputs:**
  - NEVER use manual JSON parsing or regex for LLM outputs
  - Always use Instructor + Pydantic for type-safe, validated responses
  - Leverage automatic retries and error correction





