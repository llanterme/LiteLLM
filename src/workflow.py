import logging
from typing import Dict, Any, TypedDict, Optional
from langgraph.graph import StateGraph, END
from .agents.research import ResearchAgent
from .agents.content import ContentGenerationAgent
from .config import Config
from .models import WorkflowState, ResearchOutput, ContentOutput

logger = logging.getLogger(__name__)


class GraphState(TypedDict):
    topic: str
    research_output: Optional[ResearchOutput]
    content_output: Optional[ContentOutput]
    error: Optional[str]


def create_workflow(config: Config) -> StateGraph:
    research_agent = ResearchAgent(config)
    content_agent = ContentGenerationAgent(config)
    
    workflow = StateGraph(GraphState)
    
    def research_node(state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("Executing research node")
            return research_agent(state)
        except Exception as e:
            logger.error(f"Error in research node: {str(e)}")
            state["error"] = f"Research failed: {str(e)}"
            return state
    
    def content_node(state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if state.get("error"):
                return state
            logger.info("Executing content generation node")
            return content_agent(state)
        except Exception as e:
            logger.error(f"Error in content node: {str(e)}")
            state["error"] = f"Content generation failed: {str(e)}"
            return state
    
    workflow.add_node("research", research_node)
    workflow.add_node("content_generation", content_node)
    
    workflow.set_entry_point("research")
    workflow.add_edge("research", "content_generation")
    workflow.add_edge("content_generation", END)
    
    return workflow.compile()


async def run_workflow(topic: str, config: Config) -> WorkflowState:
    logger.info(f"Starting workflow for topic: {topic}")
    
    workflow = create_workflow(config)
    
    initial_state = {
        "topic": topic,
        "research_output": None,
        "content_output": None,
        "error": None
    }
    
    try:
        result = await workflow.ainvoke(initial_state)
        
        final_state = WorkflowState(**result)
        
        if final_state.error:
            logger.error(f"Workflow completed with error: {final_state.error}")
        else:
            logger.info("Workflow completed successfully")
        
        return final_state
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        return WorkflowState(
            topic=topic,
            error=f"Workflow execution failed: {str(e)}"
        )


def run_workflow_sync(topic: str, config: Config) -> WorkflowState:
    logger.info(f"Starting workflow for topic: {topic}")
    
    workflow = create_workflow(config)
    
    initial_state = {
        "topic": topic,
        "research_output": None,
        "content_output": None,
        "error": None
    }
    
    try:
        result = workflow.invoke(initial_state)
        
        final_state = WorkflowState(**result)
        
        if final_state.error:
            logger.error(f"Workflow completed with error: {final_state.error}")
        else:
            logger.info("Workflow completed successfully")
        
        return final_state
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        return WorkflowState(
            topic=topic,
            error=f"Workflow execution failed: {str(e)}"
        )