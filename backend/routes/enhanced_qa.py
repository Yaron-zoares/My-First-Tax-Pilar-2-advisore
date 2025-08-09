"""
Enhanced AI Question-Answering routes for Pilar2
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from config.settings import settings
from backend.utils.logger import get_logger
from backend.services.enhanced_qa_engine import EnhancedQAEngine

logger = get_logger(__name__)
router = APIRouter()

class EnhancedQuestionRequest(BaseModel):
    """Enhanced request model for Q&A"""
    question: str
    file_path: Optional[str] = None
    context: Optional[str] = None
    language: str = "en"  # en, he
    include_sources: bool = True
    use_ai_enhancement: bool = True
    detail_level: str = "detailed"  # basic, detailed, comprehensive

class EnhancedQuestionResponse(BaseModel):
    """Enhanced response model for Q&A"""
    answer: str
    confidence: float
    sources: List[str]
    related_questions: List[str]
    language: str
    ai_enhanced: bool = False
    question_type: str = "general"
    recommendations: List[str] = []
    risk_analysis: Dict[str, Any] = {}
    next_steps: List[str] = []

@router.post("/enhanced-ask", response_model=EnhancedQuestionResponse)
async def enhanced_ask_question(request: EnhancedQuestionRequest):
    """
    Ask an enhanced question about financial data with AI capabilities
    """
    try:
        # Initialize Enhanced QA engine
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Load data if file path provided
        if request.file_path:
            enhanced_qa_engine.update_data_from_file(request.file_path)
        
        # Get enhanced answer
        if request.use_ai_enhancement:
            response = enhanced_qa_engine.ask_enhanced_question(
                question=request.question,
                language=request.language
            )
        else:
            # Fallback to basic QA
            response = enhanced_qa_engine.ask_question(
                question=request.question,
                language=request.language
            )
        
        logger.info(f"Enhanced question answered: {request.question[:50]}...")
        
        return EnhancedQuestionResponse(
            answer=response['answer'],
            confidence=response['confidence'],
            sources=response.get('sources', []),
            related_questions=response.get('related_questions', []),
            language=request.language,
            ai_enhanced=response.get('ai_enhanced', False),
            question_type=response.get('question_type', 'general'),
            recommendations=response.get('recommendations', []),
            risk_analysis=response.get('risk_analysis', {}),
            next_steps=response.get('next_steps', [])
        )
        
    except Exception as e:
        logger.error(f"Enhanced QA error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing enhanced question"
        )

@router.get("/enhanced-suggestions")
async def get_enhanced_suggestions(
    category: Optional[str] = None,
    language: str = "en"
):
    """
    Get enhanced question suggestions
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        suggestions = enhanced_qa_engine.get_enhanced_suggestions(
            category=category,
            language=language
        )
        
        return {
            "suggestions": suggestions,
            "language": language,
            "category": category
        }
        
    except Exception as e:
        logger.error(f"Enhanced suggestions error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting enhanced suggestions"
        )

@router.get("/enhanced-categories")
async def get_enhanced_categories(language: str = "en"):
    """
    Get enhanced Q&A categories
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        categories = enhanced_qa_engine.get_enhanced_categories(language=language)
        
        return {
            "categories": categories,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Enhanced categories error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error getting enhanced categories"
        )

@router.post("/ai-ask")
async def ai_ask_question(request: EnhancedQuestionRequest):
    """
    Ask a question using AI capabilities only
    """
    try:
        # Initialize Enhanced QA engine
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Load data if file path provided
        if request.file_path:
            enhanced_qa_engine.update_data_from_file(request.file_path)
        
        # Force AI enhancement
        response = enhanced_qa_engine.ask_enhanced_question(
            question=request.question,
            language=request.language
        )
        
        logger.info(f"AI question answered: {request.question[:50]}...")
        
        return EnhancedQuestionResponse(
            answer=response['answer'],
            confidence=response['confidence'],
            sources=response.get('sources', []),
            related_questions=response.get('related_questions', []),
            language=request.language,
            ai_enhanced=True,
            question_type=response.get('question_type', 'general'),
            recommendations=response.get('recommendations', []),
            risk_analysis=response.get('risk_analysis', {}),
            next_steps=response.get('next_steps', [])
        )
        
    except Exception as e:
        logger.error(f"AI QA error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing AI question"
        )

@router.get("/knowledge-base")
async def get_knowledge_base():
    """
    Get available knowledge base information
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        knowledge_base = enhanced_qa_engine.knowledge_base
        
        return {
            "knowledge_base": knowledge_base,
            "available_sources": list(knowledge_base.keys()),
            "total_sources": len(knowledge_base)
        }
        
    except Exception as e:
        logger.error(f"Knowledge base error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving knowledge base"
        )

@router.get("/ai-status")
async def get_ai_status():
    """
    Get AI system status
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Test AI connection
        test_result = enhanced_qa_engine.test_model_connection()
        
        return {
            "ai_enabled": settings.OPENAI_API_KEY is not None,
            "current_model": enhanced_qa_engine.ai_model,
            "connection_status": test_result["success"],
            "test_result": test_result,
            "config": enhanced_qa_engine.get_ai_config()
        }
        
    except Exception as e:
        logger.error(f"AI status error: {str(e)}")
        return {
            "ai_enabled": False,
            "error": str(e)
        }

# New routes for AI model management
class AIModelConfigRequest(BaseModel):
    """Request model for AI configuration updates"""
    ai_model: Optional[str] = None
    ai_temperature: Optional[float] = None
    ai_max_tokens: Optional[int] = None

@router.post("/ai-config/update")
async def update_ai_config(request: AIModelConfigRequest):
    """
    Update AI configuration
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        enhanced_qa_engine.update_ai_config(
            ai_model=request.ai_model,
            ai_temperature=request.ai_temperature,
            ai_max_tokens=request.ai_max_tokens
        )
        
        return {
            "success": True,
            "message": "AI configuration updated successfully",
            "config": enhanced_qa_engine.get_ai_config()
        }
        
    except Exception as e:
        logger.error(f"AI config update error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating AI configuration: {str(e)}"
        )

@router.get("/ai-config/current")
async def get_current_ai_config():
    """
    Get current AI configuration
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        return enhanced_qa_engine.get_ai_config()
        
    except Exception as e:
        logger.error(f"AI config get error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting AI configuration: {str(e)}"
        )

@router.get("/ai-models/available")
async def get_available_ai_models():
    """
    Get list of available AI models
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        return {
            "models": enhanced_qa_engine.get_available_models(),
            "current_model": enhanced_qa_engine.ai_model
        }
        
    except Exception as e:
        logger.error(f"Available models error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting available models: {str(e)}"
        )

@router.post("/ai-models/test")
async def test_ai_model(model: str = Query(..., description="Model to test")):
    """
    Test connection to a specific AI model
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        test_result = enhanced_qa_engine.test_model_connection(model)
        
        return {
            "test_result": test_result,
            "model": model,
            "timestamp": test_result.get("timestamp")
        }
        
    except Exception as e:
        logger.error(f"Model test error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error testing model: {str(e)}"
        )

@router.get("/ai-models/compare")
async def compare_ai_models():
    """
    Compare different AI models
    """
    try:
        enhanced_qa_engine = EnhancedQAEngine(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        models = enhanced_qa_engine.get_available_models()
        
        # Create comparison matrix
        comparison = {
            "models": models,
            "comparison_matrix": {
                "speed": {
                    "Very Fast": ["gpt-4o-mini"],
                    "Fast": ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4o"],
                    "Medium": ["gpt-4", "gpt-4-turbo", "gpt-4-turbo-preview"]
                },
                "cost": {
                    "Low": ["gpt-3.5-turbo"],
                    "Low-Medium": ["gpt-4o-mini"],
                    "Medium": ["gpt-3.5-turbo-16k"],
                    "Medium-High": ["gpt-4o"],
                    "High": ["gpt-4", "gpt-4-turbo", "gpt-4-turbo-preview"]
                },
                "capability": {
                    "Basic": ["gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
                    "Advanced": ["gpt-4", "gpt-4o-mini"],
                    "Premium": ["gpt-4-turbo", "gpt-4-turbo-preview", "gpt-4o"]
                }
            },
            "recommendations": {
                "cost_optimization": ["gpt-3.5-turbo", "gpt-4o-mini"],
                "performance": ["gpt-4o", "gpt-4-turbo"],
                "complex_analysis": ["gpt-4", "gpt-4-turbo"],
                "real_time": ["gpt-4o-mini", "gpt-3.5-turbo"]
            }
        }
        
        return comparison
        
    except Exception as e:
        logger.error(f"Model comparison error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing models: {str(e)}"
        )
