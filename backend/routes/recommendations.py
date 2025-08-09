"""
AI Recommendations routes for Pilar2
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from config.settings import settings, HEBREW_TEXTS
from backend.utils.logger import get_logger
from backend.services.recommendation_engine import RecommendationEngine

logger = get_logger(__name__)
router = APIRouter()

class RecommendationRequest(BaseModel):
    """Request model for recommendations"""
    file_path: str
    recommendation_type: str = "comprehensive"  # tax, regulatory, financial, comprehensive
    include_explanations: bool = True
    language: str = "he"  # he, en

class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    recommendations: List[Dict]
    priority: str  # high, medium, low
    category: str
    explanations: List[str]
    action_items: List[str]

@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendations(request: RecommendationRequest):
    """
    Generate AI-powered recommendations
    יצירת המלצות מבוססות AI
    """
    try:
        # Initialize recommendation engine
        engine = RecommendationEngine()
        
        # Load and analyze data from file
        import pandas as pd
        from pathlib import Path
        
        # Try different possible file locations
        possible_paths = [
            settings.PROCESSED_DIR / request.file_path,
            settings.UPLOAD_DIR / request.file_path,
            Path("data/examples") / request.file_path,
            Path(request.file_path)  # Absolute path
        ]
        
        file_path = None
        for path in possible_paths:
            if path.exists():
                file_path = path
                break
        
        if not file_path or not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Load data based on file type
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            data = pd.read_excel(file_path)
        elif file_path.suffix.lower() == '.csv':
            data = pd.read_csv(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Create analysis data structure
        analysis_data = {
            'data': data,
            'file_path': str(file_path),
            'recommendation_type': request.recommendation_type,
            'language': request.language
        }
        
        # Generate recommendations
        recommendations_list = engine.generate_recommendations(
            analysis_data=analysis_data,
            recommendation_type=request.recommendation_type
        )
        
        # Format response
        response_data = {
            'recommendations': recommendations_list,
            'priority': 'medium',  # Default priority
            'category': request.recommendation_type,
            'explanations': [rec.get('explanation', '') for rec in recommendations_list if rec.get('explanation')],
            'action_items': [rec.get('action', '') for rec in recommendations_list if rec.get('action')]
        }
        
        logger.info(f"Recommendations generated for {request.file_path}")
        
        return RecommendationResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error generating recommendations"
        )

@router.get("/types")
async def get_recommendation_types():
    """
    Get available recommendation types
    קבלת סוגי המלצות זמינים
    """
    return {
        "types": {
            "tax": {
                "he": "המלצות מס",
                "en": "Tax Recommendations",
                "description": "המלצות לחישובי מס והתאמות"
            },
            "regulatory": {
                "he": "המלצות רגולטוריות",
                "en": "Regulatory Recommendations",
                "description": "המלצות לעמידה בדרישות רגולטוריות"
            },
            "financial": {
                "he": "המלצות פיננסיות",
                "en": "Financial Recommendations",
                "description": "המלצות לניהול פיננסי"
            },
            "comprehensive": {
                "he": "המלצות מקיפות",
                "en": "Comprehensive Recommendations",
                "description": "המלצות מקיפות לכל התחומים"
            }
        }
    }

@router.get("/priority/{filename}")
async def get_priority_recommendations(
    filename: str,
    priority: str = Query("high", description="Priority level")
):
    """
    Get priority recommendations for a file
    קבלת המלצות בעדיפות גבוהה לקובץ
    """
    try:
        engine = RecommendationEngine()
        
        recommendations = engine.get_priority_recommendations(
            filename=filename,
            priority=priority
        )
        
        return {
            "filename": filename,
            "priority": priority,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"Priority recommendations error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting priority recommendations"
        )

@router.post("/validate")
async def validate_recommendations(
    file_path: str,
    recommendations: List[Dict]
):
    """
    Validate recommendations against data
    אימות המלצות מול הנתונים
    """
    try:
        engine = RecommendationEngine()
        
        validation_results = engine.validate_recommendations(
            file_path=file_path,
            recommendations=recommendations
        )
        
        return {
            "validation_results": validation_results,
            "valid_count": len([r for r in validation_results if r['valid']]),
            "invalid_count": len([r for r in validation_results if not r['valid']])
        }
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error validating recommendations"
        )

@router.get("/trends")
async def get_recommendation_trends(
    days: int = Query(30, description="Number of days to analyze")
):
    """
    Get recommendation trends over time
    קבלת מגמות המלצות לאורך זמן
    """
    try:
        engine = RecommendationEngine()
        
        trends = engine.get_trends(days=days)
        
        return {
            "trends": trends,
            "period_days": days,
            "total_recommendations": trends.get("total_count", 0)
        }
        
    except Exception as e:
        logger.error(f"Trends error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting recommendation trends"
        )

@router.post("/custom")
async def generate_custom_recommendations(
    file_path: str,
    focus_areas: List[str],
    constraints: Optional[Dict] = None,
    language: str = "he"
):
    """
    Generate custom recommendations based on specific focus areas
    יצירת המלצות מותאמות אישית לפי תחומי מיקוד
    """
    try:
        engine = RecommendationEngine()
        
        recommendations = engine.generate_custom_recommendations(
            file_path=file_path,
            focus_areas=focus_areas,
            constraints=constraints,
            language=language
        )
        
        return {
            "focus_areas": focus_areas,
            "constraints": constraints,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"Custom recommendations error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error generating custom recommendations"
        )

@router.get("/categories")
async def get_recommendation_categories():
    """
    Get recommendation categories
    קבלת קטגוריות המלצות
    """
    return {
        "categories": {
            "tax_optimization": {
                "he": "אופטימיזציה של מס",
                "en": "Tax Optimization",
                "subcategories": ["depreciation", "provisions", "loss_carryforward"]
            },
            "regulatory_compliance": {
                "he": "עמידה רגולטורית",
                "en": "Regulatory Compliance",
                "subcategories": ["reporting", "disclosures", "deadlines"]
            },
            "financial_management": {
                "he": "ניהול פיננסי",
                "en": "Financial Management",
                "subcategories": ["cash_flow", "profitability", "efficiency"]
            },
            "risk_management": {
                "he": "ניהול סיכונים",
                "en": "Risk Management",
                "subcategories": ["operational", "financial", "compliance"]
            }
        }
    }

@router.get("/stats")
async def get_recommendation_stats():
    """
    Get recommendation statistics
    קבלת סטטיסטיקות המלצות
    """
    try:
        engine = RecommendationEngine()
        stats = engine.get_statistics()
        
        return {
            "statistics": stats,
            "total_recommendations": stats.get("total_count", 0),
            "average_priority": stats.get("average_priority", "medium"),
            "most_common_category": stats.get("most_common_category", "tax")
        }
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting recommendation statistics"
        )
