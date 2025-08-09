"""
Enhanced QA Engine Service
Handles advanced questions and answers with ChatGPT 3.5 integration
"""

import pandas as pd
import openai
from typing import Dict, List, Optional, Any
import logging
import re
import asyncio
from datetime import datetime

from backend.services.qa_engine import QAEngine
from config.settings import settings

logger = logging.getLogger(__name__)

class EnhancedQAEngine(QAEngine):
    """Enhanced Question and Answer engine with ChatGPT 3.5 integration"""
    
    def __init__(self, openai_api_key: str = None, data: pd.DataFrame = None, ai_model: str = "gpt-3.5-turbo", ai_temperature: float = 0.3, ai_max_tokens: int = 1000):
        """
        Initialize Enhanced QA engine
        
        Args:
            openai_api_key: OpenAI API key for ChatGPT
            data: DataFrame containing financial data
            ai_model: AI model to use (gpt-3.5-turbo, gpt-4, gpt-4-turbo, etc.)
            ai_temperature: AI creativity level (0.0-1.0)
            ai_max_tokens: Maximum tokens for AI responses
        """
        super().__init__(data)  # Initialize parent class
        
        # Initialize OpenAI client
        self.openai_api_key = openai_api_key or settings.OPENAI_API_KEY
        if self.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
            logger.warning("OpenAI API key not provided. AI features will be disabled.")
        
        # AI configuration
        self.ai_model = ai_model
        self.ai_temperature = ai_temperature
        self.ai_max_tokens = ai_max_tokens
        
        # Enhanced QA patterns
        self.enhanced_qa_patterns = self._setup_enhanced_qa_patterns()
        
        # Knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def _setup_enhanced_qa_patterns(self) -> Dict[str, Dict]:
        """Setup enhanced QA patterns for advanced question types"""
        return {
            'pillar_two_compliance': {
                'patterns': [
                    r'pillar two', r'compliance', r'ציות', r'עמוד שני', r'pillar 2'
                ],
                'keywords': ['ETR', 'Top-Up Tax', 'GloBE', 'IIR', 'UTPR', 'Safe Harbour']
            },
            'tax_calculations': {
                'patterns': [
                    r'tax calculation', r'חישוב מס', r'ETR', r'שיעור מס', r'effective tax rate'
                ],
                'keywords': ['Effective Tax Rate', 'Covered Taxes', 'GloBE Income', 'Tax Adjustments']
            },
            'regulatory_analysis': {
                'patterns': [
                    r'regulatory', r'רגולטורי', r'guidelines', r'הנחיות', r'oecd'
                ],
                'keywords': ['OECD Guidelines', 'Safe Harbours', 'Administrative Guidance']
            },
            'risk_assessment': {
                'patterns': [
                    r'risk', r'סיכון', r'exposure', r'חשיפה', r'mitigation'
                ],
                'keywords': ['Risk Assessment', 'Compliance Risk', 'Tax Risk', 'Mitigation']
            },
            'strategic_planning': {
                'patterns': [
                    r'strategy', r'אסטרטגיה', r'planning', r'תכנון', r'optimization'
                ],
                'keywords': ['Tax Planning', 'Mitigation Strategies', 'Optimization']
            }
        }
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base for enhanced Q&A"""
        return {
            'pillar_two_rules': {
                'description': 'OECD Pillar Two Global Minimum Tax Rules',
                'sources': [
                    'OECD Pillar Two Model Rules',
                    'OECD Commentary on Pillar Two',
                    'Administrative Guidance'
                ]
            },
            'tax_treaties': {
                'description': 'International Tax Treaties and Agreements',
                'sources': [
                    'OECD Model Tax Convention',
                    'Bilateral Tax Treaties',
                    'Multilateral Tax Agreements'
                ]
            },
            'regulatory_guidelines': {
                'description': 'Regulatory Guidelines and Best Practices',
                'sources': [
                    'OECD Transfer Pricing Guidelines',
                    'BEPS Action Plan',
                    'Country-by-Country Reporting'
                ]
            },
            'financial_analysis': {
                'description': 'Financial Analysis and Tax Calculations',
                'sources': [
                    'IFRS Standards',
                    'Local GAAP',
                    'Tax Accounting Standards'
                ]
            }
        }
    
    def ask_enhanced_question(self, question: str, language: str = "en") -> Dict[str, Any]:
        """
        Answer a question using enhanced capabilities with ChatGPT 3.5
        
        Args:
            question: The question to answer
            language: Language of the question (en/he)
            
        Returns:
            Dictionary containing enhanced answer and metadata
        """
        try:
            # First, try basic QA engine
            basic_response = super().ask_question(question, language)
            
            # Check if we have OpenAI client
            if not self.openai_client:
                return basic_response
            
            # Classify question type
            question_type = self._classify_enhanced_question(question.lower())
            
            # If it's a complex question, enhance with AI
            if self._is_complex_question(question, question_type):
                enhanced_answer = self._enhance_with_ai(question, basic_response, question_type, language)
                return enhanced_answer
            
            return basic_response
            
        except Exception as e:
            logger.error(f"Enhanced question answering error: {str(e)}")
            # Fallback to basic response
            return super().ask_question(question, language)
    
    def _classify_enhanced_question(self, question: str) -> str:
        """Classify the type of enhanced question"""
        for qa_type, config in self.enhanced_qa_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, question, re.IGNORECASE):
                    return qa_type
        
        return 'general'
    
    def _is_complex_question(self, question: str, question_type: str) -> bool:
        """Determine if a question is complex enough for AI enhancement"""
        # Check question length
        if len(question.split()) > 10:
            return True
        
        # Check for complex keywords
        complex_keywords = [
            'why', 'how', 'explain', 'analyze', 'compare', 'recommend',
            'למה', 'איך', 'הסבר', 'נתח', 'השווה', 'המלץ'
        ]
        
        if any(keyword in question.lower() for keyword in complex_keywords):
            return True
        
        # Check question type
        if question_type in ['pillar_two_compliance', 'regulatory_analysis', 'strategic_planning']:
            return True
        
        return False
    
    def _enhance_with_ai(self, question: str, basic_response: Dict[str, Any], question_type: str, language: str) -> Dict[str, Any]:
        """Enhance basic response with AI capabilities"""
        try:
            # Prepare context
            context = self._prepare_ai_context(question, basic_response, question_type)
            
            # Build prompt
            prompt = self._build_ai_prompt(question, context, language)
            
            # Get AI response
            ai_response = self._get_ai_response(prompt, language)
            
            # Combine basic and AI responses
            enhanced_response = basic_response.copy()
            enhanced_response['answer'] = self._combine_responses(basic_response['answer'], ai_response, language)
            enhanced_response['ai_enhanced'] = True
            enhanced_response['question_type'] = question_type
            enhanced_response['confidence'] = min(basic_response['confidence'] + 0.2, 1.0)  # Boost confidence
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"AI enhancement error: {str(e)}")
            return basic_response
    
    def _prepare_ai_context(self, question: str, basic_response: Dict[str, Any], question_type: str) -> Dict[str, Any]:
        """Prepare context for AI analysis"""
        context = {
            'question': question,
            'basic_answer': basic_response['answer'],
            'question_type': question_type,
            'data_summary': self._get_data_summary(),
            'knowledge_base': self.knowledge_base.get(question_type, {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add financial data context if available
        if self.data is not None and not self.data.empty:
            context['data_columns'] = list(self.data.columns)
            context['data_shape'] = self.data.shape
            context['data_summary_stats'] = self._get_summary_statistics()
        
        return context
    
    def _get_data_summary(self) -> Dict[str, Any]:
        """Get summary of available data"""
        if self.data is None or self.data.empty:
            return {'status': 'no_data', 'message': 'No data available'}
        
        summary = {
            'status': 'available',
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_types': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict()
        }
        
        # Add financial indicators
        financial_columns = [col for col in self.data.columns 
                           if any(keyword in col.lower() for keyword in ['revenue', 'income', 'tax', 'profit', 'expense'])]
        
        if financial_columns:
            summary['financial_columns'] = financial_columns
            summary['financial_summary'] = self.data[financial_columns].describe().to_dict()
        
        return summary
    
    def _get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for numerical columns"""
        if self.data is None or self.data.empty:
            return {}
        
        numerical_columns = self.data.select_dtypes(include=['number']).columns
        if len(numerical_columns) == 0:
            return {}
        
        return self.data[numerical_columns].describe().to_dict()
    
    def _build_ai_prompt(self, question: str, context: Dict[str, Any], language: str) -> str:
        """Build AI prompt for enhanced analysis"""
        if language == "he":
            system_prompt = """אתה מומחה בינלאומי למיסוי ועמוד שני של OECD. 
            תפקידך לספק תשובות מפורטות ומדויקות לשאלות על מיסוי בינלאומי, 
            חישובי ETR, ציות לעמוד שני, וניתוח סיכונים.
            
            השתמש בנתונים הפיננסיים והקשר שסופק כדי לתת תשובה מקיפה ומעשית."""
            
            user_prompt = f"""
            שאלה: {question}
            
            הקשר:
            - תשובה בסיסית: {context['basic_answer']}
            - סוג שאלה: {context['question_type']}
            - סיכום נתונים: {context['data_summary']}
            
            אנא ספק תשובה מפורטת ומעשית שמרחיבה את התשובה הבסיסית עם:
            1. הסבר מעמיק יותר
            2. המלצות מעשיות
            3. ניתוח סיכונים רלוונטי
            4. צעדים הבאים מומלצים
            """
        else:
            system_prompt = """You are an international tax expert specializing in OECD Pillar Two. 
            Your role is to provide detailed and accurate answers to questions about international taxation, 
            ETR calculations, Pillar Two compliance, and risk analysis.
            
            Use the provided financial data and context to give comprehensive and practical answers."""
            
            user_prompt = f"""
            Question: {question}
            
            Context:
            - Basic answer: {context['basic_answer']}
            - Question type: {context['question_type']}
            - Data summary: {context['data_summary']}
            
            Please provide a detailed and practical answer that enhances the basic answer with:
            1. Deeper explanation
            2. Practical recommendations
            3. Relevant risk analysis
            4. Recommended next steps
            """
        
        return {
            'system': system_prompt,
            'user': user_prompt
        }
    
    def _get_ai_response(self, prompt: Dict[str, str], language: str) -> str:
        """Get response from ChatGPT using configured model"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": prompt['system']},
                    {"role": "user", "content": prompt['user']}
                ],
                temperature=self.ai_temperature,
                max_tokens=self.ai_max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error with model {self.ai_model}: {str(e)}")
            # Fallback to gpt-3.5-turbo if the selected model fails
            if self.ai_model != "gpt-3.5-turbo":
                logger.info(f"Falling back to gpt-3.5-turbo due to error with {self.ai_model}")
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": prompt['system']},
                            {"role": "user", "content": prompt['user']}
                        ],
                        temperature=self.ai_temperature,
                        max_tokens=self.ai_max_tokens
                    )
                    return response.choices[0].message.content
                except Exception as fallback_error:
                    logger.error(f"Fallback model also failed: {str(fallback_error)}")
                    return ""
            return ""
    
    def _combine_responses(self, basic_answer: str, ai_answer: str, language: str) -> str:
        """Combine basic and AI responses"""
        if not ai_answer:
            return basic_answer
        
        if language == "he":
            separator = "\n\n**הרחבה מתקדמת:**\n"
        else:
            separator = "\n\n**Enhanced Analysis:**\n"
        
        return basic_answer + separator + ai_answer
    
    def get_enhanced_suggestions(self, category: str = None, language: str = "en") -> List[str]:
        """Get enhanced question suggestions"""
        suggestions = []
        
        if language == "he":
            suggestions.extend([
                "מהו שיעור המס האפקטיבי של החברה?",
                "האם החברה עומדת בתנאי Safe Harbour לפי עמוד שני?",
                "מהו הסיכון לחשיפה ל-Top-Up Tax?",
                "איך משפיעים הסכמי המס על חישוב ה-ETR?",
                "מהי האסטרטגיה האופטימלית לתכנון מס בינלאומי?",
                "האם יש צורך בהגשת GIR Report?",
                "מהי המשמעות של Administrative Guidance החדש?",
                "איך אפשר להפחית את הסיכון לחשיפה למס נוסף?"
            ])
        else:
            suggestions.extend([
                "What is the company's effective tax rate?",
                "Does the company qualify for Safe Harbour under Pillar Two?",
                "What is the risk of exposure to Top-Up Tax?",
                "How do tax treaties affect ETR calculations?",
                "What is the optimal strategy for international tax planning?",
                "Is there a need to file a GIR Report?",
                "What is the significance of the new Administrative Guidance?",
                "How can we reduce the risk of exposure to additional tax?"
            ])
        
        return suggestions
    
    def get_enhanced_categories(self, language: str = "en") -> Dict[str, Any]:
        """Get enhanced question categories"""
        if language == "he":
            return {
                "pillar_two_compliance": {
                    "name": "ציות עמוד שני",
                    "description": "שאלות על ציות לתקנות עמוד שני של OECD",
                    "questions": [
                        "האם החברה עומדת בתנאי Safe Harbour?",
                        "מהו הסיכון ל-Top-Up Tax?",
                        "האם יש צורך בהגשת GIR Report?"
                    ]
                },
                "tax_calculations": {
                    "name": "חישובי מס",
                    "description": "שאלות על חישובי מס ושיעורי מס אפקטיביים",
                    "questions": [
                        "מהו שיעור המס האפקטיבי?",
                        "איך מחשבים ETR?",
                        "מה הם Tax Adjustments?"
                    ]
                },
                "strategic_planning": {
                    "name": "תכנון אסטרטגי",
                    "description": "שאלות על תכנון מס אסטרטגי",
                    "questions": [
                        "מהי האסטרטגיה האופטימלית?",
                        "איך להפחית סיכוני מס?",
                        "מה הצעדים הבאים המומלצים?"
                    ]
                }
            }
        else:
            return {
                "pillar_two_compliance": {
                    "name": "Pillar Two Compliance",
                    "description": "Questions about OECD Pillar Two compliance",
                    "questions": [
                        "Does the company qualify for Safe Harbour?",
                        "What is the Top-Up Tax exposure risk?",
                        "Is there a need to file a GIR Report?"
                    ]
                },
                "tax_calculations": {
                    "name": "Tax Calculations",
                    "description": "Questions about tax calculations and effective tax rates",
                    "questions": [
                        "What is the effective tax rate?",
                        "How is ETR calculated?",
                        "What are the Tax Adjustments?"
                    ]
                },
                "strategic_planning": {
                    "name": "Strategic Planning",
                    "description": "Questions about strategic tax planning",
                    "questions": [
                        "What is the optimal strategy?",
                        "How to reduce tax risks?",
                        "What are the recommended next steps?"
                    ]
                }
            }
    
    def update_data_from_file(self, file_path: str):
        """Update data from file path"""
        try:
            from pathlib import Path
            from backend.services.csv_fixer import CSVFixer
            from backend.services.excel_fixer import ExcelFixer
            
            file_path_obj = Path(file_path)
            if file_path_obj.exists():
                if file_path_obj.suffix.lower() == '.csv':
                    self.data = CSVFixer.fix_malformed_csv(file_path_obj)
                elif file_path_obj.suffix.lower() in ['.xlsx', '.xls']:
                    self.data = ExcelFixer.fix_malformed_excel(file_path_obj)
                else:
                    import pandas as pd
                    self.data = pd.read_csv(file_path_obj)
                
                logger.info(f"Data updated from file: {file_path}")
            else:
                logger.warning(f"File not found: {file_path}")
                
        except Exception as e:
            logger.error(f"Error updating data from file: {str(e)}")
            raise
    
    def update_ai_config(self, ai_model: str = None, ai_temperature: float = None, ai_max_tokens: int = None):
        """Update AI configuration"""
        if ai_model is not None:
            self.ai_model = ai_model
            logger.info(f"AI model updated to: {ai_model}")
        
        if ai_temperature is not None:
            self.ai_temperature = ai_temperature
            logger.info(f"AI temperature updated to: {ai_temperature}")
        
        if ai_max_tokens is not None:
            self.ai_max_tokens = ai_max_tokens
            logger.info(f"AI max tokens updated to: {ai_max_tokens}")
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get current AI configuration"""
        return {
            "ai_model": self.ai_model,
            "ai_temperature": self.ai_temperature,
            "ai_max_tokens": self.ai_max_tokens,
            "ai_enabled": self.openai_client is not None
        }
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available AI models with their specifications"""
        return [
            {
                "model": "gpt-3.5-turbo",
                "description": "Fast and cost-effective for most tasks",
                "max_tokens": "4,096",
                "cost": "Low",
                "speed": "Fast",
                "best_for": "General Q&A, basic analysis"
            },
            {
                "model": "gpt-3.5-turbo-16k",
                "description": "Extended context for longer conversations",
                "max_tokens": "16,384",
                "cost": "Medium",
                "speed": "Fast",
                "best_for": "Long documents, complex analysis"
            },
            {
                "model": "gpt-4",
                "description": "Most capable model for complex reasoning",
                "max_tokens": "8,192",
                "cost": "High",
                "speed": "Medium",
                "best_for": "Complex analysis, strategic planning"
            },
            {
                "model": "gpt-4-turbo",
                "description": "Latest GPT-4 with improved performance",
                "max_tokens": "128,000",
                "cost": "High",
                "speed": "Medium",
                "best_for": "Advanced analysis, large documents"
            },
            {
                "model": "gpt-4-turbo-preview",
                "description": "Preview of latest GPT-4 features",
                "max_tokens": "128,000",
                "cost": "High",
                "speed": "Medium",
                "best_for": "Cutting-edge features, testing"
            },
            {
                "model": "gpt-4o",
                "description": "Latest multimodal model with enhanced capabilities",
                "max_tokens": "128,000",
                "cost": "Medium-High",
                "speed": "Fast",
                "best_for": "Multimodal analysis, advanced reasoning"
            },
            {
                "model": "gpt-4o-mini",
                "description": "Faster and more cost-effective GPT-4o",
                "max_tokens": "128,000",
                "cost": "Low-Medium",
                "speed": "Very Fast",
                "best_for": "Quick responses, cost optimization"
            }
        ]
    
    def test_model_connection(self, model: str = None) -> Dict[str, Any]:
        """Test connection to a specific AI model"""
        test_model = model or self.ai_model
        
        try:
            # Simple test prompt
            test_prompt = {
                "system": "You are a helpful assistant. Respond with 'Connection successful'.",
                "user": "Test connection"
            }
            
            response = self.openai_client.chat.completions.create(
                model=test_model,
                messages=[
                    {"role": "system", "content": test_prompt['system']},
                    {"role": "user", "content": test_prompt['user']}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            return {
                "success": True,
                "model": test_model,
                "response": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "model": test_model,
                "error": str(e),
                "message": f"Failed to connect to {test_model}"
            }
