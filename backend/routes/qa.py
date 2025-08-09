"""
AI Question-Answering routes for Pilar2
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from config.settings import settings, ENGLISH_TEXTS
from backend.utils.logger import get_logger
from backend.services.qa_engine import QAEngine

logger = get_logger(__name__)
router = APIRouter()

class QuestionRequest(BaseModel):
    """Request model for Q&A"""
    question: str
    file_path: Optional[str] = None
    context: Optional[str] = None
    language: str = "en"  # en, he
    include_sources: bool = True

class QuestionResponse(BaseModel):
    """Response model for Q&A"""
    answer: str
    confidence: float
    sources: List[str]
    related_questions: List[str]
    language: str

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about financial data
    Asking a question about financial data
    """
    try:
        # Initialize QA engine
        qa_engine = QAEngine()
        
        # Get answer
        response = qa_engine.get_answer(
            question=request.question,
            file_path=request.file_path,
            context=request.context,
            language=request.language,
            include_sources=request.include_sources
        )
        
        logger.info(f"Question answered: {request.question[:50]}...")
        
        return QuestionResponse(
            answer=response['answer'],
            confidence=response['confidence'],
            sources=response.get('sources', []),
            related_questions=response.get('related_questions', []),
            language=request.language
        )
        
    except Exception as e:
        logger.error(f"QA error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing question"
        )

@router.get("/suggestions")
async def get_question_suggestions(
    file_path: Optional[str] = None,
    category: Optional[str] = None,
    language: str = "en"
):
    """
    Get suggested questions based on data
    Getting suggested questions based on data
    """
    try:
        qa_engine = QAEngine()
        
        suggestions = qa_engine.get_suggestions(
            file_path=file_path,
            category=category,
            language=language
        )
        
        return {
            "suggestions": suggestions,
            "language": language,
            "category": category
        }
        
    except Exception as e:
        logger.error(f"Suggestions error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting suggestions"
        )

@router.get("/categories")
async def get_qa_categories():
    """
    Get available Q&A categories
    Getting available Q&A categories
    """
    return {
        "categories": {
            "financial_analysis": {
                "en": "Financial Analysis",
                "questions": [
                    "What is the net profit?",
                    "What is the revenue trend?",
                    "What is the asset to liability ratio?"
                ]
            },
            "tax_calculations": {
                "en": "Tax Calculations",
                "questions": [
                    "What is the income tax payment?",
                    "What are the tax adjustments?",
                    "What is the depreciation for tax purposes?"
                ]
            },
            "regulatory_compliance": {
                "en": "Regulatory Compliance",
                "questions": [
                    "What are the regulatory requirements?",
                    "Which reports are required?",
                    "What are the filing deadlines?"
                ]
            },
            "trends_analysis": {
                "en": "Trends Analysis",
                "questions": [
                    "What is the trend in the last year?",
                    "How does it compare to previous period?",
                    "What is the forecast for next year?"
                ]
            }
        }
    }

@router.post("/batch")
async def batch_questions(questions: List[QuestionRequest]):
    """
    Ask multiple questions in batch
    Asking multiple questions in batch
    """
    try:
        qa_engine = QAEngine()
        results = []
        
        for request in questions:
            try:
                response = qa_engine.get_answer(
                    question=request.question,
                    file_path=request.file_path,
                    context=request.context,
                    language=request.language,
                    include_sources=request.include_sources
                )
                
                results.append({
                    "question": request.question,
                    "status": "success",
                    "response": response
                })
                
            except Exception as e:
                results.append({
                    "question": request.question,
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "results": results,
            "total_questions": len(questions),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"])
        }
        
    except Exception as e:
        logger.error(f"Batch QA error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error in batch question processing"
        )

@router.get("/history")
async def get_qa_history(
    limit: int = Query(10, description="Number of recent questions to retrieve")
):
    """
    Get recent question history
    Getting recent question history
    """
    try:
        qa_engine = QAEngine()
        history = qa_engine.get_history(limit=limit)
        
        return {
            "history": history,
            "total_count": len(history)
        }
        
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving QA history"
        )

@router.delete("/history")
async def clear_qa_history():
    """
    Clear question history
    Clearing question history
    """
    try:
        qa_engine = QAEngine()
        qa_engine.clear_history()
        
        return {
            "message": "QA history cleared successfully"
        }
        
    except Exception as e:
        logger.error(f"Clear history error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error clearing QA history"
        )

@router.get("/stats")
async def get_qa_stats():
    """
    Get Q&A statistics
    Getting Q&A statistics
    """
    try:
        qa_engine = QAEngine()
        stats = qa_engine.get_statistics()
        
        return {
            "statistics": stats,
            "total_questions": stats.get("total_questions", 0),
            "average_confidence": stats.get("average_confidence", 0.0),
            "most_common_categories": stats.get("most_common_categories", [])
        }
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving QA statistics"
        )
