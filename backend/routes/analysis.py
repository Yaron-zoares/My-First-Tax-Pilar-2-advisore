"""
Financial analysis routes for Pilar2
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from config.settings import settings, ENGLISH_TEXTS, FINANCIAL_CATEGORIES, TAX_ADJUSTMENTS
from backend.utils.logger import get_logger
from backend.services.tax_calculator import TaxCalculator
from backend.services.financial_analyzer import FinancialAnalyzer
from backend.services.csv_fixer import CSVFixer
from backend.services.excel_fixer import ExcelFixer

logger = get_logger(__name__)
router = APIRouter()

class AnalysisRequest(BaseModel):
    """Request model for financial analysis"""
    file_path: str
    analysis_type: str = "comprehensive"  # basic, comprehensive, tax_focused
    include_adjustments: bool = True
    include_recommendations: bool = True

class AnalysisResponse(BaseModel):
    """Response model for financial analysis"""
    summary: Dict
    details: Dict
    adjustments: List[Dict]
    recommendations: List[str]
    charts: Dict
    calculation_explanations: Dict = {}  # Add calculation explanations

@router.post("/financial", response_model=AnalysisResponse)
async def analyze_financial_data(request: AnalysisRequest):
    """
    Analyze financial data from uploaded file
    Analyzing financial data from uploaded file
    """
    try:
        # Load data - try multiple possible locations
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
                detail=f"Data file not found: {request.file_path}"
            )
        
        # Load data based on file type
        if data_path.suffix.lower() in ['.xlsx', '.xls']:
            # Try to fix malformed Excel first
            df = ExcelFixer.fix_malformed_excel(data_path)
            
            if df is None:
                # If fixing failed, try standard methods
                try:
                    df = pd.read_excel(data_path)
                except Exception as e:
                    logger.warning(f"Standard Excel reading failed: {str(e)}")
                    try:
                        # Try with different sheet names
                        df = pd.read_excel(data_path, sheet_name=0)
                    except Exception as e2:
                        logger.error(f"All Excel reading methods failed: {str(e2)}")
                        raise HTTPException(
                            status_code=400,
                            detail=f"Unable to read Excel file: {str(e2)}"
                        )
        elif data_path.suffix.lower() == '.csv':
            # Try to fix malformed CSV first
            df = CSVFixer.fix_malformed_csv(data_path)
            
            if df is None:
                # If fixing failed, try standard methods
                try:
                    df = pd.read_csv(data_path)
                except Exception as e:
                    logger.warning(f"Standard CSV reading failed: {str(e)}")
                    try:
                        # Try with different encoding and error handling
                        df = pd.read_csv(data_path, encoding='utf-8', on_bad_lines='skip')
                    except Exception as e2:
                        logger.warning(f"UTF-8 CSV reading failed: {str(e2)}")
                        try:
                            # Try with latin-1 encoding
                            df = pd.read_csv(data_path, encoding='latin-1', on_bad_lines='skip')
                        except Exception as e3:
                            logger.error(f"All CSV reading methods failed: {str(e3)}")
                            raise HTTPException(
                                status_code=400,
                                detail=f"Unable to read CSV file: {str(e3)}"
                            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please use CSV or Excel files."
            )
        
        # Initialize analyzers
        analyzer = FinancialAnalyzer(df)
        tax_calc = TaxCalculator()
        
        # Perform analysis
        analysis_result = analyzer.analyze(request.analysis_type)
        
        # Calculate tax adjustments if requested
        adjustments = []
        if request.include_adjustments:
            adjustments = tax_calc.calculate_adjustments(df)
        
        # Generate recommendations
        recommendations = []
        if request.include_recommendations:
            recommendations = analyzer.generate_recommendations(analysis_result)
        
        # Create charts data
        charts = analyzer.create_charts_data()
        
        logger.info(f"Financial analysis completed for {request.file_path}")
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif hasattr(obj, 'item'):  # numpy types
                return obj.item()
            else:
                return obj
        
        # Convert all data to JSON-serializable types
        summary = convert_numpy_types(analysis_result['summary'])
        details = convert_numpy_types(analysis_result['details'])
        adjustments = convert_numpy_types(adjustments)
        charts = convert_numpy_types(charts)
        
        return AnalysisResponse(
            summary=summary,
            details=details,
            adjustments=adjustments,
            recommendations=recommendations,
            charts=charts,
            calculation_explanations=analysis_result.get('calculation_explanations', {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error performing financial analysis"
        )

@router.get("/summary/{filename}")
async def get_analysis_summary(filename: str):
    """
    Get analysis summary for a specific file
    Getting analysis summary for a specific file
    """
    try:
        data_path = settings.PROCESSED_DIR / filename
        if not data_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        df = pd.read_csv(data_path)
        analyzer = FinancialAnalyzer(df)
        
        # Perform basic analysis to get summary
        analysis_result = analyzer.analyze("basic")
        summary = analysis_result.get('summary', {})
        
        return {
            "filename": filename,
            "summary": summary,
            "total_rows": len(df),
            "total_columns": len(df.columns)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summary error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error generating summary"
        )

@router.get("/categories")
async def get_financial_categories():
    """
    Get available financial categories
    Getting available financial categories
    """
    return {
        "categories": FINANCIAL_CATEGORIES,
        "adjustments": TAX_ADJUSTMENTS
    }

@router.post("/tax-calculations")
async def calculate_tax_adjustments(
    file_path: str,
    include_depreciation: bool = True,
    include_provisions: bool = True,
    include_capital_gains: bool = True
):
    """
    Calculate tax adjustments for financial data
    Calculating tax adjustments for financial data
    """
    try:
        data_path = settings.PROCESSED_DIR / file_path
        if not data_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        df = pd.read_csv(data_path)
        tax_calc = TaxCalculator()
        
        adjustments = tax_calc.calculate_adjustments(
            df,
            include_depreciation=include_depreciation,
            include_provisions=include_provisions,
            include_capital_gains=include_capital_gains
        )
        
        total_adjustment = sum(adj['amount'] for adj in adjustments)
        
        return {
            "adjustments": adjustments,
            "total_adjustment": total_adjustment,
            "tax_impact": total_adjustment * settings.TAX_RATES['corporate']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tax calculation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error calculating tax adjustments"
        )

@router.get("/trends/{filename}")
async def analyze_trends(
    filename: str,
    period: str = Query("annual", description="Analysis period")
):
    """
    Analyze financial trends
    Analyzing financial trends
    """
    try:
        data_path = settings.PROCESSED_DIR / filename
        if not data_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        df = pd.read_csv(data_path)
        analyzer = FinancialAnalyzer(df)
        
        # Perform analysis to get trends
        analysis_result = analyzer.analyze("comprehensive")
        trends = analysis_result.get('details', {}).get('trends', {})
        
        return {
            "filename": filename,
            "period": period,
            "trends": trends
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Trend analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error analyzing trends"
        )

@router.get("/comparison")
async def compare_periods(
    file1: str,
    file2: str,
    comparison_type: str = Query("year_over_year", description="Comparison type")
):
    """
    Compare financial data between periods
    Comparing financial data between periods
    """
    try:
        data_path1 = settings.PROCESSED_DIR / file1
        data_path2 = settings.PROCESSED_DIR / file2
        
        if not data_path1.exists() or not data_path2.exists():
            raise HTTPException(
                status_code=404,
                detail="One or both files not found"
            )
        
        df1 = pd.read_csv(data_path1)
        df2 = pd.read_csv(data_path2)
        
        analyzer1 = FinancialAnalyzer(df1)
        analyzer2 = FinancialAnalyzer(df2)
        
        # Perform analysis on both datasets
        analysis1 = analyzer1.analyze("basic")
        analysis2 = analyzer2.analyze("basic")
        
        # Simple comparison
        comparison = {
            "file1_summary": analysis1.get('summary', {}),
            "file2_summary": analysis2.get('summary', {}),
            "comparison_type": comparison_type
        }
        
        return {
            "file1": file1,
            "file2": file2,
            "comparison_type": comparison_type,
            "comparison": comparison
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error performing comparison"
        )
