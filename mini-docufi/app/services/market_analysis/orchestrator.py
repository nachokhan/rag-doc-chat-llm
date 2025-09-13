"""
Orchestrator for the market analysis service.
"""
from app.db import get_db
from app.models import MarketAnalysis, TaskStatus
from . import researchers, synthesizers

def run_analysis(task_id: int, query: str):
    """
    Runs the market analysis, orchestrating the sub-agents.
    """
    print(f"Starting analysis for task {task_id} with query: {query}")
    db = next(get_db())
    
    try:
        # 1. Update status to IN_PROGRESS
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({
            "status": TaskStatus.IN_PROGRESS,
            "progress_updates": "Starting analysis..."
        })
        db.commit()

        # 2. Research
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({"progress_updates": "Researching internal and external data..."})
        db.commit()
        external_data = researchers.research_external_data(query)
        internal_data = researchers.research_internal_data(query)
        
        # 3. Synthesize
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({"progress_updates": "Synthesizing market size and top players..."})
        db.commit()
        market_size_report = synthesizers.synthesize_market_size(external_data + internal_data)
        top_players_report = synthesizers.synthesize_top_players(external_data + internal_data)

        # 4. Compile final report
        final_report = f"""
# Market Analysis for "{query}"

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
        print(f"Analysis for task {task_id} complete.")

    except Exception as e:
        print(f"Analysis for task {task_id} failed: {e}")
        db.query(MarketAnalysis).filter(MarketAnalysis.id == task_id).update({
            "status": TaskStatus.FAILED,
            "progress_updates": f"Analysis failed: {e}"
        })
        db.commit()
    finally:
        db.close()
