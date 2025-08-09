"""
QA Engine Service
Handles questions and answers about financial data
"""

import pandas as pd
from typing import Dict, List, Optional, Any
import logging
import re

from config.settings import FINANCIAL_CATEGORIES

logger = logging.getLogger(__name__)

class QAEngine:
    """Question and Answer engine for financial data"""
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Initialize QA engine
        
        Args:
            data: DataFrame containing financial data
        """
        self.data = data
        self.qa_patterns = self._setup_qa_patterns()
    
    def _setup_qa_patterns(self) -> Dict[str, Dict]:
        """Setup QA patterns for different types of questions"""
        return {
            'revenue': {
                'patterns': [
                    r'revenue', r'income', r'sales', r'הכנסות', r'רווחים'
                ],
                'keywords': ['revenue', 'income', 'sales', 'הכנסות', 'רווחים']
            },
            'expenses': {
                'patterns': [
                    r'expense', r'cost', r'expenditure', r'הוצאות', r'עלויות'
                ],
                'keywords': ['expense', 'cost', 'expenditure', 'הוצאות', 'עלויות']
            },
            'profit': {
                'patterns': [
                    r'profit', r'net', r'רווח', r'נתון'
                ],
                'keywords': ['profit', 'net', 'רווח', 'נתון']
            },
            'tax': {
                'patterns': [
                    r'tax', r'מס', r'מיסוי'
                ],
                'keywords': ['tax', 'מס', 'מיסוי']
            },
            'trend': {
                'patterns': [
                    r'trend', r'change', r'שינוי', r'מגמה'
                ],
                'keywords': ['trend', 'change', 'שינוי', 'מגמה']
            }
        }
    
    def ask_question(self, question: str, language: str = "en") -> Dict[str, Any]:
        """
        Answer a question about financial data
        
        Args:
            question: The question to answer
            language: Language of the question (en/he)
            
        Returns:
            Dictionary containing answer and metadata
        """
        try:
            # Check if we have data
            if self.data is None or self.data.empty:
                return {
                    'answer': "אין נתונים זמינים לניתוח. אנא העלה קובץ נתונים תחילה." if language == "he" else "No data available for analysis. Please upload a data file first.",
                    'confidence': 0.0,
                    'sources': [],
                    'related_questions': [],
                    'question_type': 'general'
                }
            
            # Analyze question
            question_type = self._classify_question(question.lower())
            
            # Generate answer based on question type
            if question_type == 'revenue':
                answer = self._answer_revenue_question(question)
            elif question_type == 'expenses':
                answer = self._answer_expense_question(question)
            elif question_type == 'profit':
                answer = self._answer_profit_question(question)
            elif question_type == 'tax':
                answer = self._answer_tax_question(question)
            elif question_type == 'trend':
                answer = self._answer_trend_question(question)
            else:
                answer = self._answer_general_question(question)
            
            # Translate answer to Hebrew if needed
            if language == "he":
                answer = self._translate_to_hebrew(answer)
            
            return {
                'answer': answer,
                'confidence': self._calculate_confidence(question, question_type),
                'sources': self._get_sources(question_type),
                'related_questions': [],
                'question_type': question_type
            }
            
        except Exception as e:
            logger.error(f"Question answering error: {str(e)}")
            error_msg = "שגיאה בעיבוד השאלה. אנא נסה שוב." if language == "he" else "Error processing question. Please try again."
            return {
                'answer': error_msg,
                'confidence': 0.0,
                'sources': [],
                'related_questions': [],
                'question_type': 'error'
            }
    
    def _classify_question(self, question: str) -> str:
        """Classify the type of question"""
        for qa_type, config in self.qa_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, question, re.IGNORECASE):
                    return qa_type
        
        return 'general'
    
    def _answer_revenue_question(self, question: str) -> str:
        """Answer revenue-related questions"""
        if self.data is None:
            return "Revenue data is not available in the current dataset."
        
        try:
            revenue_columns = [col for col in self.data.columns 
                             if 'revenue' in col.lower() or 'income' in col.lower()]
            
            if revenue_columns:
                total_revenue = 0
                for col in revenue_columns:
                    total_revenue += self._safe_convert_to_float(self.data[col]).sum()
                
                # Add jurisdiction breakdown if available
                if 'Jurisdiction' in self.data.columns:
                    jurisdiction_revenue = self.data.groupby('Jurisdiction')[revenue_columns[0]].apply(lambda x: self._safe_convert_to_float(x).sum())
                    breakdown = "\nהתפלגות לפי מדינות:\n" + "\n".join([f"{jur}: ₪{rev:,.0f}" for jur, rev in jurisdiction_revenue.items()])
                    return f"הכנסה כוללת: ₪{total_revenue:,.0f}{breakdown}"
                else:
                    return f"הכנסה כוללת: ₪{total_revenue:,.0f}"
            else:
                return "לא נמצאו עמודות הכנסות בנתונים."
                
        except Exception as e:
            logger.error(f"Revenue question error: {str(e)}")
            return "לא ניתן לחשב הכנסות מהנתונים הזמינים."
    
    def _safe_convert_to_float(self, series):
        """Safely convert pandas series to float"""
        try:
            return pd.to_numeric(series, errors='coerce').fillna(0)
        except:
            return pd.Series([0] * len(series), index=series.index)
    
    def _answer_expense_question(self, question: str) -> str:
        """Answer expense-related questions"""
        if self.data is None:
            return "Expense data is not available in the current dataset."
        
        try:
            # Find expense columns (including fees and royalties)
            expense_columns = [col for col in self.data.columns 
                             if 'expense' in col.lower() or 'cost' in col.lower() or 'fees' in col.lower() or 'royalties' in col.lower()]
            
            if expense_columns:
                total_expenses = 0
                expense_breakdown = {}
                
                for col in expense_columns:
                    col_total = self._safe_convert_to_float(self.data[col]).sum()
                    total_expenses += col_total
                    expense_breakdown[col] = col_total
                
                # Create breakdown
                breakdown = "\nהתפלגות הוצאות:\n" + "\n".join([f"{col}: ₪{amount:,.0f}" for col, amount in expense_breakdown.items()])
                
                return f"הוצאות כוללות: ₪{total_expenses:,.0f}{breakdown}"
            else:
                return "לא נמצאו עמודות הוצאות בנתונים."
                
        except Exception as e:
            logger.error(f"Expense question error: {str(e)}")
            return "לא ניתן לחשב הוצאות מהנתונים הזמינים."
    
    def _answer_profit_question(self, question: str) -> str:
        """Answer profit-related questions"""
        if self.data is None:
            return "Profit data is not available in the current dataset."
        
        try:
            # Calculate revenue and expenses
            revenue_columns = [col for col in self.data.columns 
                             if 'revenue' in col.lower() or 'income' in col.lower()]
            expense_columns = [col for col in self.data.columns 
                             if 'expense' in col.lower() or 'cost' in col.lower()]
            
            total_revenue = self.data[revenue_columns].sum().sum() if revenue_columns else 0
            total_expenses = self.data[expense_columns].sum().sum() if expense_columns else 0
            net_profit = total_revenue - total_expenses
            
            return f"The net profit is ₪{net_profit:,.0f} (Revenue: ₪{total_revenue:,.0f}, Expenses: ₪{total_expenses:,.0f})."
                
        except Exception as e:
            logger.error(f"Profit question error: {str(e)}")
            return "Unable to calculate profit from the available data."
    
    def _answer_tax_question(self, question: str) -> str:
        """Answer tax-related questions"""
        if self.data is None:
            return "Tax data is not available in the current dataset."
        
        try:
            # Check for specific tax columns in the data
            tax_columns = [col for col in self.data.columns 
                          if 'tax' in col.lower() or 'מס' in col]
            covered_tax_columns = [col for col in self.data.columns 
                                  if 'covered tax' in col.lower()]
            
            # Check for revenue and income columns
            revenue_columns = [col for col in self.data.columns 
                             if 'revenue' in col.lower() or 'income' in col.lower()]
            globe_income_columns = [col for col in self.data.columns 
                                   if 'globe income' in col.lower()]
            
            # Check for ETR (Effective Tax Rate) columns
            etr_columns = [col for col in self.data.columns 
                          if 'etr' in col.lower()]
            
            # Analyze the data structure
            analysis_parts = []
            
            # Check if we have direct tax data
            if tax_columns:
                total_tax = self.data[tax_columns].sum().sum()
                analysis_parts.append(f"Total tax from data: ₪{total_tax:,.0f}")
            
            if covered_tax_columns:
                total_covered_tax = self.data[covered_tax_columns].sum().sum()
                analysis_parts.append(f"Total covered taxes: ₪{total_covered_tax:,.0f}")
            
            # Check revenue/income
            if revenue_columns:
                total_revenue = self.data[revenue_columns].sum().sum()
                analysis_parts.append(f"Total revenue: ₪{total_revenue:,.0f}")
            
            if globe_income_columns:
                total_globe_income = self.data[globe_income_columns].sum().sum()
                analysis_parts.append(f"Total GloBE income: ₪{total_globe_income:,.0f}")
            
            # Check ETR
            if etr_columns:
                # Get average ETR
                etr_values = []
                for col in etr_columns:
                    for value in self.data[col]:
                        if isinstance(value, str) and '%' in value:
                            try:
                                etr_values.append(float(value.replace('%', '')) / 100)
                            except:
                                pass
                        elif isinstance(value, (int, float)):
                            etr_values.append(value / 100 if value > 1 else value)
                
                if etr_values:
                    avg_etr = sum(etr_values) / len(etr_values)
                    analysis_parts.append(f"Average ETR: {avg_etr:.1%}")
            
            # Check for zero tax reasons
            zero_tax_reasons = []
            
            # Check if all tax values are zero
            if tax_columns:
                all_tax_zero = all(self.data[col].sum() == 0 for col in tax_columns)
                if all_tax_zero:
                    zero_tax_reasons.append("All tax values in the dataset are zero")
            
            # Check if there's no income
            if revenue_columns and globe_income_columns:
                total_income = self.data[revenue_columns].sum().sum() + self.data[globe_income_columns].sum().sum()
                if total_income == 0:
                    zero_tax_reasons.append("No income reported in the dataset")
            
            # Check for qualified status
            qualified_columns = [col for col in self.data.columns 
                               if 'qualified' in col.lower()]
            if qualified_columns:
                qualified_count = sum(1 for col in qualified_columns 
                                    for value in self.data[col] 
                                    if str(value).lower() == 'yes')
                total_entities = len(self.data)
                if qualified_count == total_entities:
                    zero_tax_reasons.append("All entities have qualified status (may affect tax calculations)")
            
            # Construct response
            if analysis_parts:
                response = "Tax Analysis:\n" + "\n".join(f"• {part}" for part in analysis_parts)
                
                if zero_tax_reasons:
                    response += "\n\nPossible reasons for zero tax:\n" + "\n".join(f"• {reason}" for reason in zero_tax_reasons)
                
                return response
            else:
                return "Tax data found but unable to analyze specific values. Please check the data structure."
                
        except Exception as e:
            logger.error(f"Tax question error: {str(e)}")
            return f"Unable to calculate tax information from the available data. Error: {str(e)}"
    
    def _answer_trend_question(self, question: str) -> str:
        """Answer trend-related questions"""
        if self.data is None:
            return "Trend data is not available in the current dataset."
        
        try:
            # Check if temporal data is available
            date_columns = [col for col in self.data.columns if 'date' in col.lower()]
            
            if date_columns:
                return f"Temporal data is available with {len(self.data)} periods for trend analysis."
            else:
                return "No temporal data available for trend analysis."
                
        except Exception as e:
            logger.error(f"Trend question error: {str(e)}")
            return "Unable to analyze trends from the available data."
    
    def _answer_general_question(self, question: str) -> str:
        """Answer general questions"""
        return "I can help you with questions about revenue, expenses, profit, taxes, and trends. Please ask a specific question about the financial data."
    
    def _calculate_confidence(self, question: str, question_type: str) -> float:
        """Calculate confidence score for the answer"""
        try:
            # Base confidence
            confidence = 0.5
            
            # Increase confidence based on data availability
            if self.data is not None and not self.data.empty:
                confidence += 0.3
            
            # Increase confidence based on question type match
            if question_type != 'general':
                confidence += 0.2
            
            # Cap at 1.0
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Confidence calculation error: {str(e)}")
            return 0.5
    
    def _get_sources(self, question_type: str) -> List[str]:
        """Get sources for the answer"""
        sources = []
        
        if self.data is not None:
            sources.append("Financial dataset")
        
        if question_type in self.qa_patterns:
            sources.append(f"{question_type.title()} analysis")
        
        sources.append("Pilar2 Financial Analysis System")
        
        return sources
    
    def _translate_to_hebrew(self, text: str) -> str:
        """Translate common financial terms to Hebrew"""
        translations = {
            "Tax Analysis:": "ניתוח מס:",
            "Total tax from data:": "סך המס מהנתונים:",
            "Total covered taxes:": "סך המסים המכוסים:",
            "Total revenue:": "סך ההכנסות:",
            "Total GloBE income:": "סך הכנסות GloBE:",
            "Average ETR:": "שיעור מס אפקטיבי ממוצע:",
            "Possible reasons for zero tax:": "סיבות אפשריות למס אפס:",
            "All tax values in the dataset are zero": "כל ערכי המס בנתונים הם אפס",
            "No income reported in the dataset": "לא דווחו הכנסות בנתונים",
            "All entities have qualified status": "לכל הגופים יש מעמד מוסמך",
            "Tax data found but unable to analyze": "נמצאו נתוני מס אך לא ניתן לנתח",
            "Revenue data is not available": "נתוני הכנסות אינם זמינים",
            "Expense data is not available": "נתוני הוצאות אינם זמינים",
            "Profit data is not available": "נתוני רווח אינם זמינים",
            "Trend data is not available": "נתוני מגמות אינם זמינים",
            "Unable to calculate": "לא ניתן לחשב",
            "from the available data": "מהנתונים הזמינים",
            "Error processing question": "שגיאה בעיבוד השאלה",
            "Please try again": "אנא נסה שוב"
        }
        
        translated_text = text
        for english, hebrew in translations.items():
            translated_text = translated_text.replace(english, hebrew)
        
        return translated_text
    
    def update_data(self, data: pd.DataFrame):
        """Update the data used for answering questions"""
        self.data = data
        logger.info("QA engine data updated")
    
    def get_answer(self, question: str, file_path: Optional[str] = None, context: Optional[str] = None, language: str = "en", include_sources: bool = True) -> Dict[str, Any]:
        """
        Get answer for a question
        
        Args:
            question: The question to answer
            file_path: Optional file path to load data from
            context: Optional context information
            language: Language of the question (en/he)
            include_sources: Whether to include sources in response
            
        Returns:
            Dictionary containing answer and metadata
        """
        try:
            # Load data from file if provided
            if file_path and (self.data is None or self.data.empty):
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
            
            # Get answer
            result = self.ask_question(question, language)
            
            # Add related questions
            result['related_questions'] = self._get_related_questions(question, language)
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting answer: {str(e)}")
            return {
                'answer': "שגיאה בעיבוד השאלה. אנא נסה שוב." if language == "he" else "Error processing question. Please try again.",
                'confidence': 0.0,
                'sources': [],
                'related_questions': [],
                'question_type': 'error'
            }
    
    def get_suggestions(self, file_path: Optional[str] = None, category: Optional[str] = None, language: str = "en") -> List[str]:
        """
        Get suggested questions
        
        Args:
            file_path: Optional file path
            category: Optional category filter
            language: Language for suggestions
            
        Returns:
            List of suggested questions
        """
        if language == "he":
            suggestions = [
                "מהי ההכנסה הכוללת של החברה?",
                "מהם ההוצאות העיקריות?",
                "מהו הרווח הנקי?",
                "איך מתחלקים הנתונים לפי מדינות?",
                "מהו שיעור המס האפקטיבי?",
                "אילו עלויות יש לתאם?",
                "מהי מגמת הרווחים?",
                "איך מתחלקים הנתונים לפי סגמנטים עסקיים?"
            ]
        else:
            suggestions = [
                "What is the total revenue of the company?",
                "What are the main expenses?",
                "What is the net profit?",
                "How is the data distributed by jurisdictions?",
                "What is the effective tax rate?",
                "What costs need to be adjusted?",
                "What is the profit trend?",
                "How is the data distributed by business segments?"
            ]
        
        return suggestions
    
    def _get_related_questions(self, question: str, language: str) -> List[str]:
        """Get related questions based on the current question"""
        if language == "he":
            return [
                "מהי ההכנסה הכוללת?",
                "מהם ההוצאות העיקריות?",
                "מהו הרווח הנקי?"
            ]
        else:
            return [
                "What is the total revenue?",
                "What are the main expenses?",
                "What is the net profit?"
            ]
    
    def get_available_questions(self) -> List[str]:
        """Get list of example questions that can be answered"""
        return [
            "What is the total revenue?",
            "What are the total expenses?",
            "What is the net profit?",
            "What is the tax liability?",
            "Are there any trends in the data?",
            "What is the profit margin?",
            "What are the main expense categories?"
        ]
