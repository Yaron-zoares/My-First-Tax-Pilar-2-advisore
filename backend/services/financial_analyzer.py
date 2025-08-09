"""
Financial Analyzer Service
Provides comprehensive financial analysis capabilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from config.settings import FINANCIAL_CATEGORIES, TAX_ADJUSTMENTS

logger = logging.getLogger(__name__)

class FinancialAnalyzer:
    """Financial data analyzer for comprehensive analysis"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize analyzer with financial data
        
        Args:
            data: DataFrame containing financial data
        """
        self.data = data
        self.summary = {}
        self.details = {}
        self.calculation_explanations = {}  # Store calculation explanations
    
    def _safe_convert_to_float(self, series):
        """
        Safely convert pandas series to float, handling various data formats
        
        Args:
            series: Pandas series to convert
            
        Returns:
            Series with numeric values, non-numeric values become 0
        """
        try:
            # Handle DataFrame input
            if isinstance(series, pd.DataFrame):
                # If it's a DataFrame, try to convert the first column
                if len(series.columns) > 0:
                    series = series.iloc[:, 0]
                else:
                    return pd.Series([0] * len(series), index=series.index)
            
            # First try direct conversion
            return pd.to_numeric(series, errors='coerce').fillna(0)
        except Exception as e:
            logger.warning(f"Error converting series to float: {str(e)}")
            # Fallback: try to clean the data first
            try:
                # Remove commas and other non-numeric characters
                cleaned_series = series.astype(str).str.replace(',', '').str.replace('%', '')
                return pd.to_numeric(cleaned_series, errors='coerce').fillna(0)
            except Exception as e2:
                logger.error(f"Failed to convert series to float: {str(e2)}")
                return pd.Series([0] * len(series), index=series.index)
        
    def analyze(self, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Perform financial analysis based on type
        
        Args:
            analysis_type: Type of analysis (basic, comprehensive, tax_focused)
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Basic analysis always performed
            self._perform_basic_analysis()
            
            if analysis_type == "comprehensive":
                self._perform_comprehensive_analysis()
            elif analysis_type == "tax_focused":
                self._perform_tax_focused_analysis()
            
            return {
                "summary": self.summary,
                "details": self.details,
                "analysis_type": analysis_type,
                "calculation_explanations": self.calculation_explanations
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
    
    def _perform_basic_analysis(self):
        """Perform basic financial analysis"""
        try:
            # Log data info for debugging
            logger.info(f"Data shape: {self.data.shape}")
            logger.info(f"Data columns: {list(self.data.columns)}")
            logger.info(f"Data head: {self.data.head()}")
            
            # Calculate basic metrics
            if not self.data.empty:
                # For Pillar2 data, look for GloBE Income and Covered Taxes
                if 'GloBE Income' in self.data.columns:
                    self.summary['revenue'] = self._safe_convert_to_float(self.data['GloBE Income']).sum()
                    logger.info(f"Found GloBE Income column, revenue: {self.summary['revenue']}")
                elif 'Revenue' in self.data.columns:
                    self.summary['revenue'] = self._safe_convert_to_float(self.data['Revenue']).sum()
                    logger.info(f"Found Revenue column, revenue: {self.summary['revenue']}")
                elif 'Revenue ($)' in self.data.columns:
                    self.summary['revenue'] = self._safe_convert_to_float(self.data['Revenue ($)']).sum()
                    logger.info(f"Found Revenue ($) column, revenue: {self.summary['revenue']}")
                elif any('income' in col.lower() for col in self.data.columns):
                    revenue_columns = [col for col in self.data.columns if 'income' in col.lower()]
                    if revenue_columns:
                        self.summary['revenue'] = self._safe_convert_to_float(self.data[revenue_columns]).sum().sum()
                        logger.info(f"Found income columns: {revenue_columns}, revenue: {self.summary['revenue']}")
                else:
                    logger.warning("No revenue/income columns found in data")
                    self.summary['revenue'] = 0
                
                # Tax analysis
                if 'Covered Taxes' in self.data.columns:
                    self.summary['taxes'] = self._safe_convert_to_float(self.data['Covered Taxes']).sum()
                    logger.info(f"Found Covered Taxes column, taxes: {self.summary['taxes']}")
                    self._add_tax_calculation_explanation("actual", "Covered Taxes", self.summary['taxes'])
                elif 'Tax Expense' in self.data.columns:
                    self.summary['taxes'] = self._safe_convert_to_float(self.data['Tax Expense']).sum()
                    logger.info(f"Found Tax Expense column, taxes: {self.summary['taxes']}")
                    self._add_tax_calculation_explanation("actual", "Tax Expense", self.summary['taxes'])
                elif 'Tax Amount' in self.data.columns:
                    self.summary['taxes'] = self._safe_convert_to_float(self.data['Tax Amount']).sum()
                    logger.info(f"Found Tax Amount column, taxes: {self.summary['taxes']}")
                    self._add_tax_calculation_explanation("actual", "Tax Amount", self.summary['taxes'])
                else:
                    logger.warning("No tax columns found in data - will calculate estimated taxes")
                    self.summary['taxes'] = 0
                
                # ETR analysis - will be calculated after tax calculations
                if 'ETR' in self.data.columns:
                    # Convert percentage strings to numbers
                    etr_values = []
                    for val in self.data['ETR']:
                        try:
                            if isinstance(val, str):
                                etr_values.append(float(val.replace('%', '')) / 100)
                            else:
                                etr_values.append(float(val))
                        except:
                            etr_values.append(0)
                    
                    if etr_values:
                        self.summary['average_etr'] = sum(etr_values) / len(etr_values)
                        self.summary['min_etr'] = min(etr_values)
                        self.summary['max_etr'] = max(etr_values)
                
                # Top-up tax analysis
                if 'Top-Up Tax' in self.data.columns:
                    self.summary['top_up_tax'] = self._safe_convert_to_float(self.data['Top-Up Tax']).sum()
                
                # Expense analysis
                expense_columns = [col for col in self.data.columns if 'expense' in col.lower() or 'cost' in col.lower() or 'fees' in col.lower() or 'royalties' in col.lower()]
                if expense_columns:
                    total_expenses = 0
                    for col in expense_columns:
                        if col not in ['Tax Expense', 'Tax Amount']:  # Exclude tax expense from general expenses
                            total_expenses += self._safe_convert_to_float(self.data[col]).sum()
                    self.summary['expenses'] = total_expenses
                    logger.info(f"Found expense columns: {expense_columns}, total expenses: {total_expenses}")
                else:
                    logger.warning("No expense columns found in data")
                    self.summary['expenses'] = 0
                
                # Net profit calculation
                revenue = self.summary.get('revenue', 0)
                expenses = self.summary.get('expenses', 0)
                taxes = self.summary.get('taxes', 0)
                self.summary['net_profit'] = revenue - expenses - taxes
                
                # Calculate estimated taxes if no tax data was found
                if taxes == 0 and revenue > 0 and expenses > 0:
                    estimated_net_income = revenue - expenses
                    if estimated_net_income > 0:
                        # Use standard corporate tax rate of 23%
                        estimated_taxes = estimated_net_income * 0.23
                        self.summary['taxes'] = estimated_taxes
                        self.summary['estimated_taxes'] = True
                        logger.info(f"Calculated estimated taxes: {estimated_taxes:,.0f} based on net income of {estimated_net_income:,.0f}")
                        
                        # Add detailed explanation for estimated tax calculation
                        self._add_tax_calculation_explanation("estimated", estimated_net_income, estimated_taxes)
                        
                        # Recalculate net profit with estimated taxes
                        self.summary['net_profit'] = estimated_net_income - estimated_taxes
                
                # Basic ratios
                if revenue > 0:
                    self.summary['tax_rate'] = (self.summary.get('taxes', 0) / revenue) * 100
                    self.summary['expense_ratio'] = (expenses / revenue) * 100
                    self.summary['profit_margin'] = (self.summary['net_profit'] / revenue) * 100
                
                # Calculate ETR after all tax calculations are complete
                if 'ETR' not in self.data.columns:
                    # Calculate estimated ETR if not provided in data
                    if self.summary.get('net_profit', 0) > 0 and self.summary.get('taxes', 0) > 0:
                        # ETR should be calculated on pre-tax income, not net profit
                        pre_tax_income = self.summary['net_profit'] + self.summary['taxes']
                        self.summary['average_etr'] = (self.summary['taxes'] / pre_tax_income) * 100
                        logger.info(f"Calculated estimated ETR: {self.summary['average_etr']:.2f}%")
                        
                        # Add detailed explanation for ETR calculation
                        self._add_etr_calculation_explanation("estimated", pre_tax_income, self.summary['taxes'], self.summary['average_etr'])
                    else:
                        self.summary['average_etr'] = 0
                
                # Jurisdiction analysis
                if 'Jurisdiction' in self.data.columns:
                    self.summary['jurisdictions'] = self.data['Jurisdiction'].nunique()
                    self.summary['entities'] = len(self.data)
                
        except Exception as e:
            logger.error(f"Basic analysis error: {str(e)}")
            # Provide fallback values
            self.summary = {
                'revenue': 0,
                'expenses': 0,
                'taxes': 0,
                'net_profit': 0,
                'error': str(e)
            }
    
    def _perform_comprehensive_analysis(self):
        """Perform comprehensive financial analysis"""
        try:
            # Trend analysis
            self._analyze_trends()
            
            # Category analysis
            self._analyze_categories()
            
            # Risk assessment
            self._assess_risks()
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {str(e)}")
    
    def _perform_tax_focused_analysis(self):
        """Perform tax-focused analysis"""
        try:
            # Tax-related metrics
            self._calculate_tax_metrics()
            
            # Tax efficiency analysis
            self._analyze_tax_efficiency()
            
        except Exception as e:
            logger.error(f"Tax analysis error: {str(e)}")
    
    def _analyze_trends(self):
        """Analyze financial trends"""
        try:
            # Simple trend calculation if date column exists
            date_columns = [col for col in self.data.columns if 'date' in col.lower()]
            if date_columns:
                self.details['trends'] = {
                    'has_temporal_data': True,
                    'periods_analyzed': len(self.data)
                }
            else:
                self.details['trends'] = {
                    'has_temporal_data': False,
                    'message': 'No temporal data available for trend analysis'
                }
                
        except Exception as e:
            logger.error(f"Trend analysis error: {str(e)}")
    
    def _analyze_categories(self):
        """Analyze financial categories"""
        try:
            categories = {}
            
            # For Pillar2 data, analyze by jurisdiction and business segment
            if 'Jurisdiction' in self.data.columns:
                # Try different revenue columns
                revenue_column = None
                for col in ['GloBE Income', 'Revenue', 'Revenue ($)']:
                    if col in self.data.columns:
                        revenue_column = col
                        break
                
                if revenue_column:
                    jurisdiction_totals = self.data.groupby('Jurisdiction')[revenue_column].apply(lambda x: self._safe_convert_to_float(x).sum())
                    # Clean NaN values for JSON serialization
                    jurisdiction_totals_clean = jurisdiction_totals.fillna(0)
                    categories['jurisdiction'] = {
                        'totals': jurisdiction_totals_clean.to_dict(),
                        'count': len(jurisdiction_totals)
                    }
                else:
                    logger.warning("No revenue column found for jurisdiction analysis")
            
            if 'Business Segment' in self.data.columns:
                # Try different revenue columns
                revenue_column = None
                for col in ['GloBE Income', 'Revenue', 'Revenue ($)']:
                    if col in self.data.columns:
                        revenue_column = col
                        break
                
                if revenue_column:
                    segment_totals = self.data.groupby('Business Segment')[revenue_column].apply(lambda x: self._safe_convert_to_float(x).sum())
                    # Clean NaN values for JSON serialization
                    segment_totals_clean = segment_totals.fillna(0)
                    categories['business_segment'] = {
                        'totals': segment_totals_clean.to_dict(),
                        'count': len(segment_totals)
                    }
                else:
                    logger.warning("No revenue column found for business segment analysis")
            
            self.details['categories'] = categories
            
        except Exception as e:
            logger.error(f"Category analysis error: {str(e)}")
    
    def _assess_risks(self):
        """Assess financial risks"""
        try:
            risks = []
            
            # Tax rate risk
            if self.summary.get('average_etr', 0) < 0.15:
                risks.append("Low effective tax rate detected")
            
            # Top-up tax risk
            if self.summary.get('top_up_tax', 0) > 0:
                risks.append("Top-up tax liability detected")
            
            # Jurisdiction concentration risk
            if 'Jurisdiction' in self.data.columns:
                jurisdiction_counts = self.data['Jurisdiction'].value_counts()
                if len(jurisdiction_counts) < 3:
                    risks.append("Jurisdiction concentration risk")
            
            # Regulatory status risk
            if 'Regulatory Status' in self.data.columns:
                inactive_count = (self.data['Regulatory Status'] == 'Inactive').sum()
                if inactive_count > 0:
                    risks.append(f"{inactive_count} entities with inactive regulatory status")
            
            self.details['risks'] = risks
            
        except Exception as e:
            logger.error(f"Risk assessment error: {str(e)}")
    
    def _calculate_tax_metrics(self):
        """Calculate tax-related metrics"""
        try:
            tax_metrics = {}
            
            # Effective tax rate calculation
            if self.summary.get('net_profit', 0) > 0:
                # Simplified ETR calculation
                tax_metrics['effective_tax_rate'] = 0.23  # Default corporate rate
                tax_metrics['tax_liability'] = self.summary['net_profit'] * 0.23
            
            self.details['tax_metrics'] = tax_metrics
            
        except Exception as e:
            logger.error(f"Tax metrics calculation error: {str(e)}")
    
    def _analyze_tax_efficiency(self):
        """Analyze tax efficiency"""
        try:
            efficiency_metrics = {}
            
            # Tax efficiency score (simplified)
            if self.summary.get('revenue', 0) > 0:
                efficiency_metrics['tax_efficiency_score'] = 0.85  # Placeholder
                efficiency_metrics['optimization_opportunities'] = [
                    "Consider tax-advantaged investments",
                    "Review depreciation strategies",
                    "Evaluate tax loss harvesting opportunities"
                ]
            
            self.details['tax_efficiency'] = efficiency_metrics
            
        except Exception as e:
            logger.error(f"Tax efficiency analysis error: {str(e)}")
    
    def generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """
        Generate recommendations based on analysis
        
        Args:
            analysis_result: Results from financial analysis
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        try:
            summary = analysis_result.get('summary', {})
            
            # Revenue and profitability recommendations
            revenue = summary.get('revenue', 0)
            profit_margin = summary.get('profit_margin', 0)
            tax_rate = summary.get('tax_rate', 0)
            
            if revenue > 0:
                if profit_margin < 10:
                    recommendations.append("Consider cost optimization strategies to improve profit margins")
                
                if profit_margin < 5:
                    recommendations.append("Review pricing strategies and operational efficiency")
                
                if revenue < 1000000:  # 1M threshold
                    recommendations.append("Explore revenue diversification opportunities")
                
                # Tax efficiency recommendations
                if tax_rate > 20:
                    recommendations.append("Review tax planning strategies to optimize effective tax rate")
                
                if summary.get('average_etr', 0) > 15:
                    recommendations.append("Consider tax-efficient investment strategies")
            
            # Jurisdiction-specific recommendations
            jurisdictions = summary.get('jurisdictions', 0)
            if jurisdictions > 1:
                recommendations.append("Implement cross-border tax compliance monitoring")
                recommendations.append("Review transfer pricing policies across jurisdictions")
            
            # Top-up tax recommendations
            if summary.get('top_up_tax', 0) > 0:
                recommendations.append("Address top-up tax obligations through strategic planning")
                recommendations.append("Review qualified status and safe harbour provisions")
            
            # ETR analysis recommendations
            if summary.get('max_etr', 0) - summary.get('min_etr', 0) > 5:
                recommendations.append("Standardize tax rates across jurisdictions for consistency")
            
            # Risk management recommendations
            if summary.get('entities', 0) > 5:
                recommendations.append("Implement centralized financial reporting and monitoring")
            
            # General recommendations
            recommendations.append("Regular financial monitoring and reporting recommended")
            recommendations.append("Consider implementing automated financial analysis tools")
            recommendations.append("Establish quarterly tax compliance reviews")
            
            # Estimated tax recommendations
            if summary.get('estimated_taxes', False):
                recommendations.append("⚠️ Tax calculations are estimated - review actual tax data for accuracy")
                recommendations.append("Consider adding tax expense columns to your data for more precise analysis")
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            recommendations.append("Error generating recommendations")
        
        return recommendations
    
    def create_charts_data(self) -> Dict[str, Any]:
        """
        Create data for charts and visualizations
        
        Returns:
            Dictionary containing chart data
        """
        charts_data = {}
        
        try:
            # Jurisdiction distribution pie chart
            if 'Jurisdiction' in self.data.columns:
                # Try different revenue columns
                revenue_column = None
                for col in ['GloBE Income', 'Revenue', 'Revenue ($)']:
                    if col in self.data.columns:
                        revenue_column = col
                        break
                
                if revenue_column:
                    jurisdiction_totals = self.data.groupby('Jurisdiction')[revenue_column].apply(lambda x: self._safe_convert_to_float(x).sum())
                    charts_data['jurisdiction_pie'] = {
                        'labels': jurisdiction_totals.index.tolist(),
                        'values': jurisdiction_totals.values.tolist()
                    }
            
            # ETR comparison bar chart
            if 'ETR' in self.data.columns and 'Jurisdiction' in self.data.columns:
                etr_data = []
                for _, row in self.data.iterrows():
                    try:
                        etr_value = float(str(row['ETR']).replace('%', ''))
                        etr_data.append({
                            'jurisdiction': row['Jurisdiction'],
                            'etr': etr_value
                        })
                    except:
                        continue
                
                if etr_data:
                    charts_data['etr_comparison'] = {
                        'labels': [item['jurisdiction'] for item in etr_data],
                        'values': [item['etr'] for item in etr_data]
                    }
            
            # Revenue vs Taxes scatter plot data
            revenue_column = None
            tax_column = None
            
            # Find revenue column
            for col in ['GloBE Income', 'Revenue', 'Revenue ($)']:
                if col in self.data.columns:
                    revenue_column = col
                    break
            
            # Find tax column
            for col in ['Covered Taxes', 'Tax Expense', 'Tax Amount']:
                if col in self.data.columns:
                    tax_column = col
                    break
            
            if revenue_column and tax_column:
                charts_data['revenue_tax_scatter'] = {
                    'x': self._safe_convert_to_float(self.data[revenue_column]).tolist(),
                    'y': self._safe_convert_to_float(self.data[tax_column]).tolist(),
                    'labels': self.data['Jurisdiction'].tolist() if 'Jurisdiction' in self.data.columns else []
                }
            
            # Top-up tax analysis
            if 'Top-Up Tax' in self.data.columns:
                top_up_data = self.data[self._safe_convert_to_float(self.data['Top-Up Tax']) > 0]
                if not top_up_data.empty:
                    charts_data['top_up_tax'] = {
                        'labels': top_up_data['Jurisdiction'].tolist(),
                        'values': self._safe_convert_to_float(top_up_data['Top-Up Tax']).tolist()
                    }
            
        except Exception as e:
            logger.error(f"Charts data creation error: {str(e)}")
            charts_data = {}
        
        return charts_data
    
    def _add_tax_calculation_explanation(self, calculation_type: str, base_value: float, tax_amount: float):
        """
        Add detailed explanation for tax calculation
        
        Args:
            calculation_type: "actual" or "estimated"
            base_value: The base value used for calculation (net income for estimated, column name for actual)
            tax_amount: The calculated tax amount
        """
        if calculation_type == "actual":
            self.calculation_explanations['tax_calculation'] = {
                'type': 'actual',
                'method': f'Direct extraction from {base_value} column',
                'method_he': f'חילוץ ישיר מעמודת {base_value}',
                'formula': f'Sum of all values in {base_value} column',
                'formula_he': f'סכום כל הערכים בעמודת {base_value}',
                'result': f'₪{tax_amount:,.0f}',
                'explanation': f'Tax amount was directly extracted from the {base_value} column in the dataset. No calculation was performed.',
                'explanation_he': f'סכום המס חולץ ישירות מעמודת {base_value} בקובץ הנתונים. לא בוצע חישוב נוסף.'
            }
        else:  # estimated
            self.calculation_explanations['tax_calculation'] = {
                'type': 'estimated',
                'method': 'Standard corporate tax rate calculation',
                'method_he': 'חישוב מס תאגידים סטנדרטי',
                'formula': f'Net Income × 23% = {base_value:,.0f} × 0.23',
                'formula_he': f'הכנסה נטו × 23% = {base_value:,.0f} × 0.23',
                'result': f'₪{tax_amount:,.0f}',
                'explanation': f'Since no tax columns were found in the data, taxes were estimated using the standard Israeli corporate tax rate of 23% applied to net income (Revenue - Expenses = {base_value:,.0f}).',
                'explanation_he': f'מכיוון שלא נמצאו עמודות מס בנתונים, המסים חושבו בשיעור מס תאגידים ישראלי סטנדרטי של 23% על הכנסה נטו (הכנסות - הוצאות = {base_value:,.0f}).'
            }
    
    def _add_etr_calculation_explanation(self, calculation_type: str, pre_tax_income: float, tax_amount: float, etr_percentage: float):
        """
        Add detailed explanation for ETR calculation
        
        Args:
            calculation_type: "actual" or "estimated"
            pre_tax_income: Pre-tax income used for calculation
            tax_amount: Tax amount
            etr_percentage: Calculated ETR percentage
        """
        if calculation_type == "estimated":
            self.calculation_explanations['etr_calculation'] = {
                'type': 'estimated',
                'method': 'Effective Tax Rate calculation',
                'method_he': 'חישוב שיעור מס אפקטיבי',
                'formula': f'(Tax Amount ÷ Pre-tax Income) × 100 = (₪{tax_amount:,.0f} ÷ ₪{pre_tax_income:,.0f}) × 100',
                'formula_he': f'(סכום המס ÷ הכנסה לפני מס) × 100 = (₪{tax_amount:,.0f} ÷ ₪{pre_tax_income:,.0f}) × 100',
                'result': f'{etr_percentage:.1f}%',
                'explanation': f'ETR was calculated as the ratio of tax amount to pre-tax income. Pre-tax income = Net Profit + Taxes = {pre_tax_income:,.0f}. This represents the effective tax burden on the company\'s earnings.',
                'explanation_he': f'שיעור המס האפקטיבי חושב כיחס בין סכום המס להכנסה לפני מס. הכנסה לפני מס = רווח נקי + מסים = {pre_tax_income:,.0f}. זה מייצג את נטל המס האפקטיבי על רווחי החברה.'
            }
        else:
            self.calculation_explanations['etr_calculation'] = {
                'type': 'actual',
                'method': 'Direct extraction from ETR column',
                'method_he': 'חילוץ ישיר מעמודת ETR',
                'formula': 'Average of ETR values from dataset',
                'formula_he': 'ממוצע ערכי ETR מקובץ הנתונים',
                'result': f'{etr_percentage:.1f}%',
                'explanation': 'ETR values were directly extracted from the ETR column in the dataset and averaged.',
                'explanation_he': 'ערכי ETR חולצו ישירות מעמודת ETR בקובץ הנתונים וחושב הממוצע שלהם.'
            }
        

