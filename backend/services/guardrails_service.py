"""
Guardrails Service for Pilar2
Provides AI response validation and quality control
"""

import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import re

try:
    from guardrails import Guard
    from guardrails.validators import ValidLength, ValidRange, ValidChoices, ValidFormat
    from pydantic import BaseModel, Field, validator
    GUARDRAILS_AVAILABLE = True
except ImportError:
    GUARDRAILS_AVAILABLE = False
    # Fallback to basic validation without guardrails
    from pydantic import BaseModel, Field, validator
    logging.warning("Guardrails not available. AI validation will be disabled.")

logger = logging.getLogger(__name__)

class PillarTwoResponseSchema(BaseModel):
    """Schema for validating Pillar Two AI responses"""
    
    answer: str = Field(..., description="The main answer to the question")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the answer")
    compliance_status: str = Field(..., description="Compliance status assessment")
    risk_level: str = Field(..., description="Risk level assessment")
    recommendations: List[str] = Field(..., description="List of actionable recommendations")
    sources: List[str] = Field(default=[], description="Sources used for the answer")
    
    @validator('compliance_status')
    def validate_compliance_status(cls, v):
        valid_statuses = ['compliant', 'non_compliant', 'requires_review', 'unknown']
        if v.lower() not in valid_statuses:
            raise ValueError(f'compliance_status must be one of {valid_statuses}')
        return v.lower()
    
    @validator('risk_level')
    def validate_risk_level(cls, v):
        valid_levels = ['low', 'medium', 'high', 'critical']
        if v.lower() not in valid_levels:
            raise ValueError(f'risk_level must be one of {valid_levels}')
        return v.lower()

class GuardrailsService:
    """Service for applying Guardrails to AI responses"""
    
    def __init__(self):
        """Initialize Guardrails service"""
        self.guardrails_available = GUARDRAILS_AVAILABLE
        self.quality_threshold = 0.8
        self.max_response_length = 2000
        
        if self.guardrails_available:
            self._setup_guardrails()
        else:
            logger.warning("Guardrails not available. Using fallback validation.")
    
    def _setup_guardrails(self):
        """Setup Guardrails validation rules"""
        if not self.guardrails_available:
            logger.info("Guardrails not available. Using fallback validation.")
            return
            
        try:
            # Create validation rules for Pillar Two responses
            self.pillar_two_guard = Guard.from_pydantic(
                PillarTwoResponseSchema,
                prompt="""
                You are a tax expert specializing in OECD Pillar Two compliance.
                Provide accurate, professional, and actionable advice.
                
                {input}
                
                Respond in the following format:
                - Answer: Clear and concise response
                - Confidence: Your confidence level (0.0-1.0)
                - Compliance Status: compliant/non_compliant/requires_review/unknown
                - Risk Level: low/medium/high/critical
                - Recommendations: List of actionable steps
                - Sources: References used
                """,
                validators={
                    "answer": [
                        ValidLength(min=50, max=self.max_response_length),
                        ValidFormat(
                            regex=r"^[A-Za-z0-9\s\.,;:!?()\[\]{}'\"-]+$",
                            on_fail="reask"
                        )
                    ],
                    "confidence": ValidRange(min=0.0, max=1.0),
                    "compliance_status": ValidChoices(
                        choices=["compliant", "non_compliant", "requires_review", "unknown"]
                    ),
                    "risk_level": ValidChoices(
                        choices=["low", "medium", "high", "critical"]
                    )
                }
            )
            
            # Create quality control guard
            self.quality_guard = Guard.from_string(
                """
                You are a quality control expert for tax advice.
                Review the following response and ensure it meets professional standards.
                
                {input}
                
                Validate that the response:
                1. Is accurate and factual
                2. Provides actionable advice
                3. Identifies risks appropriately
                4. References relevant regulations
                5. Is written in professional language
                
                If the response meets standards, return it unchanged.
                If not, provide an improved version.
                """,
                validators={
                    "response": [
                        ValidLength(min=100, max=self.max_response_length * 2),
                        ValidFormat(
                            regex=r"^[A-Za-z0-9\s\.,;:!?()\[\]{}'\"-]+$",
                            on_fail="reask"
                        )
                    ]
                }
            )
            
            logger.info("Guardrails successfully initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup Guardrails: {str(e)}")
            self.guardrails_available = False
    
    def validate_ai_response(self, response: str, question_type: str = "general") -> Dict[str, Any]:
        """
        Validate AI response using Guardrails
        
        Args:
            response: Raw AI response to validate
            question_type: Type of question for context-specific validation
            
        Returns:
            Validation result with validated response or error details
        """
        if not self.guardrails_available:
            return self._fallback_validation(response, question_type)
        
        try:
            # Apply Pillar Two specific validation
            if question_type in ["compliance", "regulatory", "risk"]:
                validation_result = self._validate_pillar_two_response(response)
            else:
                validation_result = self._validate_general_response(response)
            
            # Apply quality control
            quality_result = self._apply_quality_control(validation_result.get("validated_response", response))
            
            return {
                "success": True,
                "original_response": response,
                "validated_response": quality_result.get("validated_response", response),
                "validation_details": validation_result,
                "quality_score": quality_result.get("quality_score", 0.8),
                "warnings": validation_result.get("warnings", []),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Guardrails validation failed: {str(e)}")
            return self._fallback_validation(response, question_type)
    
    def _validate_pillar_two_response(self, response: str) -> Dict[str, Any]:
        """Validate response specifically for Pillar Two questions"""
        try:
            # Extract key information from response
            extracted_info = self._extract_pillar_two_info(response)
            
            # Validate using Pydantic schema
            validated_data = PillarTwoResponseSchema(**extracted_info)
            
            return {
                "success": True,
                "validated_response": response,
                "compliance_status": validated_data.compliance_status,
                "risk_level": validated_data.risk_level,
                "confidence": validated_data.confidence,
                "warnings": []
            }
            
        except Exception as e:
            logger.warning(f"Pillar Two validation failed: {str(e)}")
            return {
                "success": False,
                "validated_response": response,
                "warnings": [f"Validation warning: {str(e)}"],
                "compliance_status": "requires_review",
                "risk_level": "medium",
                "confidence": 0.6
            }
    
    def _validate_general_response(self, response: str) -> Dict[str, Any]:
        """Validate general AI responses"""
        try:
            # Basic validation using quality guard
            if hasattr(self, 'quality_guard'):
                try:
                    result = self.quality_guard(
                        response,
                        metadata={"question_type": "general"}
                    )
                    
                    return {
                        "success": True,
                        "validated_response": result.validated_output,
                        "warnings": []
                    }
                except Exception:
                    # Fallback if guard fails
                    pass
            
            # Fallback validation
            return {
                "success": True,
                "validated_response": response,
                "warnings": ["Using fallback validation"]
            }
            
        except Exception as e:
            logger.warning(f"General validation failed: {str(e)}")
            return {
                "success": False,
                "validated_response": response,
                "warnings": [f"Validation warning: {str(e)}"]
            }
    
    def _apply_quality_control(self, response: str) -> Dict[str, Any]:
        """Apply quality control to validated response"""
        try:
            # Check response quality metrics
            quality_score = self._calculate_quality_score(response)
            
            # Apply quality guard if score is below threshold
            if quality_score < self.quality_threshold and hasattr(self, 'quality_guard'):
                try:
                    result = self.quality_guard(response)
                    return {
                        "validated_response": result.validated_output,
                        "quality_score": quality_score,
                        "improved": True
                    }
                except Exception:
                    # Fallback if guard fails
                    pass
            
            return {
                "validated_response": response,
                "quality_score": quality_score,
                "improved": False
            }
            
        except Exception as e:
            logger.warning(f"Quality control failed: {str(e)}")
            return {
                "validated_response": response,
                "quality_score": 0.7,
                "improved": False
            }
    
    def _extract_pillar_two_info(self, response: str) -> Dict[str, Any]:
        """Extract key information from Pillar Two response"""
        # Default values
        extracted = {
            "answer": response[:500] + "..." if len(response) > 500 else response,
            "confidence": 0.8,
            "compliance_status": "requires_review",
            "risk_level": "medium",
            "recommendations": [],
            "sources": []
        }
        
        try:
            # Extract compliance status
            compliance_patterns = [
                r"compliant|ציות",
                r"non.?compliant|לא עומד|לא ציות",
                r"requires.?review|נדרש ביקורת",
                r"unknown|לא ידוע"
            ]
            
            for pattern in compliance_patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    if "compliant" in match.group().lower() or "ציות" in match.group():
                        extracted["compliance_status"] = "compliant"
                    elif "non" in match.group().lower() or "לא עומד" in match.group():
                        extracted["compliance_status"] = "non_compliant"
                    elif "review" in match.group().lower() or "ביקורת" in match.group():
                        extracted["compliance_status"] = "requires_review"
                    break
            
            # Extract risk level
            risk_patterns = [
                r"low.?risk|סיכון נמוך",
                r"medium.?risk|סיכון בינוני",
                r"high.?risk|סיכון גבוה",
                r"critical.?risk|סיכון קריטי"
            ]
            
            for pattern in risk_patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    if "low" in match.group().lower() or "נמוך" in match.group():
                        extracted["risk_level"] = "low"
                    elif "medium" in match.group().lower() or "בינוני" in match.group():
                        extracted["risk_level"] = "medium"
                    elif "high" in match.group().lower() or "גבוה" in match.group():
                        extracted["risk_level"] = "high"
                    elif "critical" in match.group().lower() or "קריטי" in match.group():
                        extracted["risk_level"] = "critical"
                    break
            
            # Extract recommendations
            rec_patterns = [
                r"recommend|המלצה",
                r"suggest|הצעה",
                r"should|צריך",
                r"consider|שקול"
            ]
            
            recommendations = []
            for pattern in rec_patterns:
                matches = re.finditer(pattern, response, re.IGNORECASE)
                for match in matches:
                    # Extract sentence containing recommendation
                    start = max(0, match.start() - 100)
                    end = min(len(response), match.end() + 100)
                    rec_text = response[start:end].strip()
                    if rec_text not in recommendations:
                        recommendations.append(rec_text)
            
            if recommendations:
                extracted["recommendations"] = recommendations[:3]  # Limit to 3 recommendations
            
            # Estimate confidence based on response quality
            confidence_factors = 0
            if len(response) > 200:
                confidence_factors += 1
            if extracted["compliance_status"] != "unknown":
                confidence_factors += 1
            if extracted["risk_level"] != "medium":
                confidence_factors += 1
            if recommendations:
                confidence_factors += 1
            
            extracted["confidence"] = min(0.95, 0.6 + (confidence_factors * 0.1))
            
        except Exception as e:
            logger.warning(f"Failed to extract Pillar Two info: {str(e)}")
        
        return extracted
    
    def _calculate_quality_score(self, response: str) -> float:
        """Calculate quality score for response"""
        score = 0.5  # Base score
        
        try:
            # Length score
            if 100 <= len(response) <= 1000:
                score += 0.2
            elif len(response) > 1000:
                score += 0.1
            
            # Professional language score
            professional_terms = [
                "compliance", "regulation", "tax", "risk", "analysis",
                "ציות", "רגולציה", "מס", "סיכון", "ניתוח"
            ]
            
            term_count = sum(1 for term in professional_terms if term.lower() in response.lower())
            score += min(0.2, term_count * 0.05)
            
            # Structure score
            if any(char in response for char in ["•", "-", "1.", "2.", "3."]):
                score += 0.1
            
            # Source reference score
            if any(word in response.lower() for word in ["source", "reference", "according to", "מקור", "על פי"]):
                score += 0.1
            
        except Exception as e:
            logger.warning(f"Quality score calculation failed: {str(e)}")
        
        return min(1.0, score)
    
    def _fallback_validation(self, response: str, question_type: str) -> Dict[str, Any]:
        """Fallback validation when Guardrails is not available"""
        logger.info("Using fallback validation")
        
        # Basic quality checks
        quality_score = self._calculate_quality_score(response)
        
        return {
            "success": True,
            "original_response": response,
            "validated_response": response,
            "validation_details": {
                "method": "fallback",
                "quality_score": quality_score
            },
            "quality_score": quality_score,
            "warnings": ["Guardrails not available - using basic validation"],
            "timestamp": datetime.now().isoformat()
        }
    
    def update_quality_threshold(self, threshold: float):
        """Update quality threshold for validation"""
        if 0.0 <= threshold <= 1.0:
            self.quality_threshold = threshold
            logger.info(f"Quality threshold updated to {threshold}")
        else:
            logger.warning(f"Invalid quality threshold: {threshold}. Must be between 0.0 and 1.0.")
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return {
            "guardrails_available": self.guardrails_available,
            "quality_threshold": self.quality_threshold,
            "max_response_length": self.max_response_length,
            "timestamp": datetime.now().isoformat()
        }
