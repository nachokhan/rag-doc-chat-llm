"""
Orchestrator for the market analysis service.
"""
import logging
from app.db import get_db
from app.models import MarketAnalysis, TaskStatus
from .researchers import run_research
from .synthesizers import synthesize_market_size, synthesize_top_players

def run_analysis(task_id: int, query: str):
    """
    Runs the market analysis, orchestrating the sub-agents.
    """
    logging.info(f"Starting analysis for task {task_id} with query: {query}")
    db = next(get_db())

    def update_progress(message: str):
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({"progress_updates": message})
        db.commit()

    try:
        # 1. Update status to IN_PROGRESS
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({"status": TaskStatus.IN_PROGRESS})
        update_progress("Starting analysis...")

        # 2. Research
        update_progress(f'Researching market size for "{query}"...')
        market_size_data = run_research(f'Market size, growth, and projections for "{query}"')

        update_progress(f'Researching top players for "{query}"...')
        top_players_data = run_research(f'Top players and competitors in "{query}"')

        # Combine research data
        combined_data = f"""--- Data on Market Size ---
{market_size_data}

--- Data on Top Players ---
{top_players_data}
"""

        # 3. Synthesize
        update_progress("Synthesizing final report...")
        market_size_report = synthesize_market_size(combined_data)
        top_players_report = synthesize_top_players(combined_data)

        # 4. Compile final report
        final_report = f"""# Market Analysis for "{query}"

## Market Size
{market_size_report}

## Top Players
{top_players_report}
        """

        # 5. Update DB with completed status and report
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({
            "status": TaskStatus.COMPLETED,
            "report": final_report,
            "progress_updates": "Analysis complete."
        })
        db.commit()
        logging.info(f"Analysis for task {task_id} complete.")

    except Exception as e:
        logging.info(f"Analysis for task {task_id} failed: {e}")
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({
            "status": TaskStatus.FAILED,
            "progress_updates": f"Analysis failed: {str(e)}"
        })
        db.commit()
    finally:
        db.close()
