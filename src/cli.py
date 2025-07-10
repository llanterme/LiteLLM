import logging
import sys
import json
from pathlib import Path
import click
from .config import Config
from .workflow import run_workflow_sync

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument('topic', required=True)
@click.option('--provider', '-p', 
              type=click.Choice(['openai', 'anthropic', 'gemini', 'ollama'], case_sensitive=False),
              help='Override LLM provider from environment')
@click.option('--output', '-o', 
              type=click.Path(),
              help='Save output to file (JSON format)')
@click.option('--verbose', '-v', 
              is_flag=True,
              help='Enable verbose logging')
def main(topic: str, provider: str, output: str, verbose: bool):
    """
    Run the AI agent workflow for a given TOPIC.
    
    The workflow will:
    1. Research the topic using the Research Agent
    2. Generate content based on the research using the Content Generation Agent
    
    Example:
        python -m src.cli "The impact of AI on education"
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        config = Config.from_env()
        
        if provider:
            config.llm_provider = provider.lower()
            click.echo(f"Using LLM provider: {config.llm_provider}")
        
        click.echo(f"\n🔍 Researching topic: {topic}")
        click.echo("=" * 50)
        
        with click.progressbar(length=2, label='Processing') as bar:
            bar.update(1)
            result = run_workflow_sync(topic, config)
            bar.update(1)
        
        if result.error:
            click.echo(f"\n❌ Error: {result.error}", err=True)
            sys.exit(1)
        
        click.echo(f"\n📚 Research Summary: {result.research_output.title}")
        click.echo("-" * 50)
        for i, point in enumerate(result.research_output.summary_points, 1):
            click.echo(f"{i}. {point}")
        
        if result.research_output.sources:
            click.echo("\n📌 Sources:")
            for source in result.research_output.sources:
                click.echo(f"- {source}")
        
        click.echo(f"\n📝 Article Summary:")
        click.echo("-" * 50)
        click.echo(result.content_output.summary)
        
        click.echo(f"\n📄 Full Article:")
        click.echo("=" * 50)
        click.echo(result.content_output.article)
        
        if output:
            output_data = {
                "topic": topic,
                "research": {
                    "title": result.research_output.title,
                    "summary_points": result.research_output.summary_points,
                    "sources": result.research_output.sources
                },
                "content": {
                    "article": result.content_output.article,
                    "summary": result.content_output.summary
                }
            }
            
            output_path = Path(output)
            output_path.write_text(json.dumps(output_data, indent=2))
            click.echo(f"\n✅ Output saved to: {output_path}")
        
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {str(e)}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()