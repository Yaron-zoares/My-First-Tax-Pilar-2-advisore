"""
Regulatory reports generation routes for Pilar2
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config.settings import settings, ENGLISH_TEXTS
from backend.utils.logger import get_logger
from backend.services.xml_generator import XMLGenerator
from backend.services.pdf_generator import PDFGenerator
from backend.services.word_generator import WordGenerator

logger = get_logger(__name__)
router = APIRouter()

class ReportRequest(BaseModel):
    """Request model for report generation"""
    file_path: str
    report_type: str  # xml, pdf, word
    report_format: str = "gir"  # gir, standard, detailed
    include_adjustments: bool = True
    include_recommendations: bool = True

@router.post("/generate")
async def generate_report(request: ReportRequest):
    """
    Generate regulatory report
    Creating regulatory report
    """
    try:
        # Validate file exists - try multiple possible locations
        from pathlib import Path
        
        # Try different possible file locations
        possible_paths = [
            settings.PROCESSED_DIR / request.file_path,
            settings.UPLOAD_DIR / request.file_path,
            Path("data/examples") / request.file_path,
            Path(request.file_path)  # Absolute path
        ]
        
        data_path = None
        for path in possible_paths:
            if path.exists():
                data_path = path
                break
        
        if not data_path or not data_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Data file not found"
            )
        
        # Generate report based on type
        if request.report_type == "xml":
            generator = XMLGenerator()
            # Load data for the report
            import pandas as pd
            if data_path.suffix.lower() in ['.xlsx', '.xls']:
                data = pd.read_excel(data_path)
            elif data_path.suffix.lower() == '.csv':
                data = pd.read_csv(data_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            # Create report data structure
            report_data = {
                'file_path': str(data_path),
                'data': data,
                'include_adjustments': request.include_adjustments
            }
            
            report_path = generator.generate_gir_xml(
                report_data,
                request.report_format
            )
        elif request.report_type == "pdf":
            generator = PDFGenerator()
            # Load data for the report
            import pandas as pd
            if data_path.suffix.lower() in ['.xlsx', '.xls']:
                data = pd.read_excel(data_path)
            elif data_path.suffix.lower() == '.csv':
                data = pd.read_csv(data_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            # Create report data structure
            report_data = {
                'file_path': str(data_path),
                'data': data,
                'include_adjustments': request.include_adjustments,
                'include_recommendations': request.include_recommendations
            }
            
            report_path = generator.generate_financial_report(
                report_data,
                request.report_format
            )
        elif request.report_type == "word":
            generator = WordGenerator()
            # Load data for the report
            import pandas as pd
            if data_path.suffix.lower() in ['.xlsx', '.xls']:
                data = pd.read_excel(data_path)
            elif data_path.suffix.lower() == '.csv':
                data = pd.read_csv(data_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            # Create report data structure
            report_data = {
                'file_path': str(data_path),
                'data': data,
                'include_adjustments': request.include_adjustments,
                'include_recommendations': request.include_recommendations
            }
            
            report_path = generator.generate_financial_report(
                report_data,
                request.report_format
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported report type: {request.report_type}"
            )
        
        logger.info(f"Report generated: {report_path}")
        
        return {
            "message": ENGLISH_TEXTS['report_generated'],
            "report_path": str(report_path),
            "report_type": request.report_type,
            "report_format": request.report_format
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error generating report"
        )

@router.get("/download/{filename}")
async def download_report(filename: str):
    """
    Download generated report
    Downloading generated report
    """
    try:
        # Check in all report directories
        report_paths = [
            settings.REPORTS_DIR / "xml" / filename,
            settings.REPORTS_DIR / "pdf" / filename,
            settings.REPORTS_DIR / "word" / filename
        ]
        
        report_path = None
        for path in report_paths:
            if path.exists():
                report_path = path
                break
        
        if not report_path:
            raise HTTPException(
                status_code=404,
                detail="Report file not found"
            )
        
        return FileResponse(
            path=report_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error downloading report"
        )

@router.get("/list")
async def list_generated_reports():
    """
    List all generated reports
    Listing all generated reports
    """
    try:
        reports = {
            "xml": [],
            "pdf": [],
            "word": []
        }
        
        # Scan all report directories
        for report_type in reports.keys():
            report_dir = settings.REPORTS_DIR / report_type
            if report_dir.exists():
                for file_path in report_dir.glob("*"):
                    if file_path.is_file():
                        reports[report_type].append({
                            "filename": file_path.name,
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime
                        })
        
        return {
            "reports": reports,
            "total_count": sum(len(reports[t]) for t in reports)
        }
        
    except Exception as e:
        logger.error(f"Error listing reports: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error listing reports"
        )

@router.delete("/delete/{filename}")
async def delete_report(filename: str):
    """
    Delete generated report
    Deleting generated report
    """
    try:
        # Check in all report directories
        report_paths = [
            settings.REPORTS_DIR / "xml" / filename,
            settings.REPORTS_DIR / "pdf" / filename,
            settings.REPORTS_DIR / "word" / filename
        ]
        
        deleted = False
        for path in report_paths:
            if path.exists():
                path.unlink()
                deleted = True
                logger.info(f"Report deleted: {filename}")
                break
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Report file not found"
            )
        
        return {
            "message": f"Report {filename} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error deleting report"
        )

@router.get("/templates")
async def get_report_templates():
    """
    Get available report templates
    Getting available report templates
    """
    return {
        "templates": {
            "gir": {
                "name": "GIR XML Report",
                "description": "Regulatory XML report",
                "formats": ["xml"]
            },
            "standard": {
                "name": "Standard Financial Report",
                "description": "Standard financial report",
                "formats": ["pdf", "word"]
            },
            "detailed": {
                "name": "Detailed Analysis Report",
                "description": "Detailed analysis report",
                "formats": ["pdf", "word"]
            },
            "tax": {
                "name": "Tax Adjustment Report",
                "description": "Tax adjustments report",
                "formats": ["pdf", "word"]
            }
        }
    }

@router.post("/batch")
async def generate_batch_reports(
    file_paths: List[str],
    report_types: List[str] = ["pdf"],
    report_format: str = "standard"
):
    """
    Generate multiple reports in batch
    Creating multiple reports in batch
    """
    try:
        results = []
        
        for file_path in file_paths:
            for report_type in report_types:
                try:
                    request = ReportRequest(
                        file_path=file_path,
                        report_type=report_type,
                        report_format=report_format
                    )
                    
                    result = await generate_report(request)
                    results.append({
                        "file": file_path,
                        "report_type": report_type,
                        "status": "success",
                        "result": result
                    })
                    
                except Exception as e:
                    results.append({
                        "file": file_path,
                        "report_type": report_type,
                        "status": "error",
                        "error": str(e)
                    })
        
        return {
            "batch_results": results,
            "total_requests": len(file_paths) * len(report_types),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"])
        }
        
    except Exception as e:
        logger.error(f"Batch generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error in batch report generation"
        )
