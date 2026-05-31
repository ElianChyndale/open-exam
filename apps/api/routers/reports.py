"""Exportable local learner reports."""

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from deps import get_repo
from services.advanced_service import weekly_report

router = APIRouter()


@router.get("/weekly")
async def read_weekly_report(format: str = "json", repo=Depends(get_repo)):
    report = weekly_report(repo)
    if format == "markdown":
        return PlainTextResponse(
            report["markdown_content"],
            headers={"Content-Disposition": f"attachment; filename={report['report_id']}.md"},
        )
    return report
