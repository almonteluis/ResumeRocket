from fastapi import APIRouter, WebSocket, BackgroundTasks, Response
from fastapi.responses import StreamingResponse
from typing import Optional
from ...services.enhanced_analyzer import EnhancedAnalyzer
from ...api.websocket import manager
import asyncio

router = APIRouter(prefix="/analysis", tags=["analysis"])
analyzer = EnhancedAnalyzer()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)

@router.post("/analyze")
async def analyze_resume(
    resume_id: int,
    job_description: str,
    background_tasks: BackgroundTasks
):
    async def process_analysis():
        analysis_id = f"analysis_{resume_id}_{int(time.time())}"
        
        # Update progress through WebSocket
        await manager.update_analysis_progress(
            analysis_id, 0, "Starting analysis..."
        )
        
        # Simulate analysis steps
        steps = [
            (20, "Extracting resume content..."),
            (40, "Analyzing skills..."),
            (60, "Evaluating experience..."),
            (80, "Generating visualizations..."),
            (100, "Analysis complete!")
        ]
        
        for progress, message in steps:
            await asyncio.sleep(1)  # Simulate processing time
            await manager.update_analysis_progress(
                analysis_id, progress, message
            )

    background_tasks.add_task(process_analysis)
    return {"message": "Analysis started"}

@router.get("/export/{analysis_id}")
async def export_report(
    analysis_id: int,
    format: str = "pdf"
) -> StreamingResponse:
    # Get analysis data
    analysis_data = {} # Get from database
    
    # Generate report
    output = analyzer.export_report(analysis_data, format)
    
    media_type = {
        'pdf': 'application/pdf',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }[format]
    
    return StreamingResponse(
        output,
        media_type=media_type,
        headers={
            'Content-Disposition': f'attachment; filename=analysis_report.{format}'
        }
    )

@router.get("/visualizations/{analysis_id}")
async def get_visualizations(
    analysis_id: int,
    chart_type: Optional[str] = None
):
    analysis_data = {} # Get from database
    
    if chart_type:
        return {
            "chart": analyzer.visualization_types[chart_type](analysis_data)
        }
    
    return {
        chart_type: viz_func(analysis_data)
        for chart_type, viz_func in analyzer.visualization_types.items()
    }