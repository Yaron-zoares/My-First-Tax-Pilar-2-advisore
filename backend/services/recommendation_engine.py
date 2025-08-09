"""
Recommendation Engine Service
Generates financial recommendations based on analysis
"""

import pandas as pd
from typing import Dict, List, Optional, Any
import logging

from config.settings import FINANCIAL_CATEGORIES, TAX_ADJUSTMENTS

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Recommendation engine for financial analysis"""
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Initialize recommendation engine
        
        Args:
            data: DataFrame containing financial data
        """
        self.data = data
        self.recommendation_rules = self._setup_recommendation_rules()
    
    def _setup_recommendation_rules(self) -> Dict[str, Dict]:
        """Setup recommendation rules for different scenarios"""
        return {
            'profit_margin': {
                'low': {'threshold': 0.05, 'recommendations': [
                    'Consider cost optimization strategies',
                    'Review pricing strategies',
                    'Analyze expense categories for reduction opportunities'
                ]},
                'medium': {'threshold': 0.15, 'recommendations': [
                    'Monitor profit margins regularly',
                    'Consider efficiency improvements',
                    'Explore revenue growth opportunities'
                ]},
                'high': {'threshold': float('inf'), 'recommendations': [
                    'Maintain current performance',
                    'Consider reinvestment opportunities',
                    'Explore expansion possibilities'
                ]}
            },
            'revenue_concentration': {
                'high': {'recommendations': [
                    'Diversify revenue sources',
                    'Develop new product lines',
                    'Explore new markets'
                ]},
                'low': {'recommendations': [
                    'Maintain diversified revenue structure',
                    'Focus on high-performing segments'
                ]}
            },
            'tax_efficiency': {
                'low': {'threshold': 0.7, 'recommendations': [
                    'Review tax planning strategies',
                    'Consider tax-advantaged investments',
                    'Consult with tax professionals'
                ]},
                'high': {'threshold': 1.0, 'recommendations': [
                    'Maintain current tax efficiency',
                    'Monitor for new tax opportunities'
                ]}
            },
            'risk_management': {
                'high': {'recommendations': [
                    'Implement risk mitigation strategies',
                    'Diversify investments',
                    'Review insurance coverage'
                ]},
                'low': {'recommendations': [
                    'Maintain current risk management practices',
                    'Regular risk assessments recommended'
                ]}
            }
        }
    
    def generate_recommendations(self, analysis_data: Dict[str, Any], recommendation_type: str = "comprehensive") -> List[Dict[str, Any]]:
        """
        Generate recommendations based on analysis data
        
        Args:
            analysis_data: Results from financial analysis
            recommendation_type: Type of recommendations (comprehensive, tax, regulatory, financial)
            
        Returns:
            List of recommendation dictionaries
        """
        try:
            recommendations = []
            
            # Create basic analysis summary if not provided
            if 'summary' not in analysis_data:
                analysis_data['summary'] = self._create_basic_summary(analysis_data.get('data', pd.DataFrame()))
            
            if recommendation_type == "comprehensive":
                recommendations.extend(self._generate_comprehensive_recommendations(analysis_data))
            elif recommendation_type == "tax":
                recommendations.extend(self._generate_tax_recommendations(analysis_data))
            elif recommendation_type == "regulatory":
                recommendations.extend(self._generate_regulatory_recommendations(analysis_data))
            elif recommendation_type == "financial":
                recommendations.extend(self._generate_financial_recommendations(analysis_data))
            else:
                recommendations.extend(self._generate_general_recommendations(analysis_data))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            return [{
                'title': 'Error in recommendation generation',
                'description': 'Unable to generate specific recommendations at this time.',
                'priority': 'medium',
                'category': 'general'
            }]
    
    def _create_basic_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Create basic financial summary from data"""
        try:
            summary = {
                'net_profit': 0,
                'total_revenue': 0,
                'total_expenses': 0,
                'profit_margin': 0,
                'row_count': len(data)
            }
            
            # Try to extract financial data from common column names
            if not data.empty:
                # Look for common financial column names
                revenue_cols = [col for col in data.columns if any(word in col.lower() for word in ['revenue', 'income', 'sales', 'תקציב', 'הכנסות'])]
                expense_cols = [col for col in data.columns if any(word in col.lower() for word in ['expense', 'cost', 'expenditure', 'הוצאות', 'עלויות'])]
                profit_cols = [col for col in data.columns if any(word in col.lower() for word in ['profit', 'net', 'רווח', 'נתון'])]
                
                # Calculate basic metrics
                if revenue_cols:
                    summary['total_revenue'] = data[revenue_cols[0]].sum() if data[revenue_cols[0]].dtype in ['int64', 'float64'] else 0
                
                if expense_cols:
                    summary['total_expenses'] = data[expense_cols[0]].sum() if data[expense_cols[0]].dtype in ['int64', 'float64'] else 0
                
                if profit_cols:
                    summary['net_profit'] = data[profit_cols[0]].sum() if data[profit_cols[0]].dtype in ['int64', 'float64'] else 0
                else:
                    summary['net_profit'] = summary['total_revenue'] - summary['total_expenses']
                
                if summary['total_revenue'] > 0:
                    summary['profit_margin'] = summary['net_profit'] / summary['total_revenue']
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating basic summary: {str(e)}")
            return {'net_profit': 0, 'total_revenue': 0, 'total_expenses': 0, 'profit_margin': 0, 'row_count': 0}
    
    def _generate_comprehensive_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        try:
            summary = analysis_data.get('summary', {})
            
            # Profit margin recommendations
            profit_margin = summary.get('profit_margin', 0)
            if profit_margin < 0.05:
                recommendations.append({
                    'title': 'Low Profit Margin',
                    'description': 'Consider implementing cost reduction strategies and reviewing pricing policies.',
                    'priority': 'high',
                    'category': 'financial'
                })
            elif profit_margin < 0.15:
                recommendations.append({
                    'title': 'Moderate Profit Margin',
                    'description': 'Focus on efficiency improvements and explore revenue growth opportunities.',
                    'priority': 'medium',
                    'category': 'financial'
                })
            
            # Revenue recommendations
            revenue = summary.get('revenue', 0)
            if revenue < 1000000:  # 1M threshold
                recommendations.append({
                    'title': 'Revenue Growth Opportunity',
                    'description': 'Consider expanding market reach and developing new revenue streams.',
                    'priority': 'medium',
                    'category': 'financial'
                })
            
            # Tax recommendations
            if 'tax_metrics' in analysis_data.get('details', {}):
                recommendations.append({
                    'title': 'Tax Planning Review',
                    'description': 'Review tax strategies with qualified professionals to optimize tax efficiency.',
                    'priority': 'medium',
                    'category': 'tax'
                })
            
        except Exception as e:
            logger.error(f"Comprehensive recommendations error: {str(e)}")
        
        return recommendations
    
    def _generate_tax_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate tax-specific recommendations"""
        recommendations = []
        
        try:
            summary = analysis_data.get('summary', {})
            net_profit = summary.get('net_profit', 0)
            
            if net_profit > 0:
                recommendations.extend([
                    {
                        'title': 'Tax Efficiency Optimization',
                        'description': 'Review depreciation strategies and consider tax-advantaged investments.',
                        'priority': 'medium',
                        'category': 'tax'
                    },
                    {
                        'title': 'Tax Loss Harvesting',
                        'description': 'Evaluate opportunities for tax loss harvesting to reduce tax liability.',
                        'priority': 'low',
                        'category': 'tax'
                    }
                ])
            else:
                recommendations.append({
                    'title': 'Tax Loss Carryforward',
                    'description': 'Consider tax loss carryforward strategies for future tax benefits.',
                    'priority': 'medium',
                    'category': 'tax'
                })
                
        except Exception as e:
            logger.error(f"Tax recommendations error: {str(e)}")
        
        return recommendations
    
    def _generate_regulatory_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate regulatory compliance recommendations"""
        recommendations = []
        
        try:
            recommendations.extend([
                {
                    'title': 'Regulatory Compliance Review',
                    'description': 'Ensure all financial reporting meets regulatory requirements.',
                    'priority': 'high',
                    'category': 'regulatory'
                },
                {
                    'title': 'Documentation Standards',
                    'description': 'Maintain comprehensive documentation for regulatory audits.',
                    'priority': 'medium',
                    'category': 'regulatory'
                },
                {
                    'title': 'Regular Compliance Monitoring',
                    'description': 'Implement regular compliance monitoring and reporting procedures.',
                    'priority': 'medium',
                    'category': 'regulatory'
                }
            ])
                
        except Exception as e:
            logger.error(f"Regulatory recommendations error: {str(e)}")
        
        return recommendations
    
    def _generate_financial_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate financial management recommendations"""
        recommendations = []
        
        try:
            summary = analysis_data.get('summary', {})
            
            # Cash flow recommendations
            recommendations.append({
                'title': 'Cash Flow Management',
                'description': 'Implement robust cash flow monitoring and forecasting systems.',
                'priority': 'high',
                'category': 'financial'
            })
            
            # Risk management
            if analysis_data.get('details', {}).get('risks'):
                recommendations.append({
                    'title': 'Risk Mitigation',
                    'description': 'Address identified financial risks through strategic planning.',
                    'priority': 'high',
                    'category': 'financial'
                })
            
            # Performance monitoring
            recommendations.append({
                'title': 'Performance Monitoring',
                'description': 'Establish regular financial performance monitoring and reporting.',
                'priority': 'medium',
                'category': 'financial'
            })
                
        except Exception as e:
            logger.error(f"Financial recommendations error: {str(e)}")
        
        return recommendations
    
    def _generate_general_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate general recommendations"""
        return [
            {
                'title': 'Regular Financial Review',
                'description': 'Conduct regular comprehensive financial reviews and analysis.',
                'priority': 'medium',
                'category': 'general'
            },
            {
                'title': 'Professional Consultation',
                'description': 'Consider consulting with financial and tax professionals for specialized advice.',
                'priority': 'low',
                'category': 'general'
            },
            {
                'title': 'Technology Integration',
                'description': 'Consider implementing automated financial analysis and reporting tools.',
                'priority': 'low',
                'category': 'general'
            }
        ]
    
    def update_data(self, data: pd.DataFrame):
        """Update the data used for recommendations"""
        self.data = data
        logger.info("Recommendation engine data updated")
    
    def get_recommendation_categories(self) -> List[str]:
        """Get available recommendation categories"""
        return ['comprehensive', 'tax', 'regulatory', 'financial']
    
    def get_priority_levels(self) -> List[str]:
        """Get available priority levels"""
        return ['high', 'medium', 'low']
