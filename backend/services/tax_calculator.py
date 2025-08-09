"""
Tax Calculator Service for Pilar2
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from config.settings import settings, TAX_ADJUSTMENTS
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class TaxCalculator:
    """Tax calculation and adjustment service"""
    
    def __init__(self):
        self.tax_rates = settings.TAX_RATES
        self.adjustments = TAX_ADJUSTMENTS
    
    def calculate_adjustments(
        self, 
        df: pd.DataFrame,
        include_depreciation: bool = True,
        include_provisions: bool = True,
        include_capital_gains: bool = True
    ) -> List[Dict]:
        """
        Calculate tax adjustments for financial data
        Tax adjustment calculation for financial data
        """
        adjustments = []
        
        try:
            # Depreciation adjustments
            if include_depreciation:
                depreciation_adj = self._calculate_depreciation_adjustments(df)
                adjustments.extend(depreciation_adj)
            
            # Provisions adjustments
            if include_provisions:
                provisions_adj = self._calculate_provisions_adjustments(df)
                adjustments.extend(provisions_adj)
            
            # Capital gains adjustments
            if include_capital_gains:
                capital_gains_adj = self._calculate_capital_gains_adjustments(df)
                adjustments.extend(capital_gains_adj)
            
            # Foreign income adjustments
            foreign_income_adj = self._calculate_foreign_income_adjustments(df)
            adjustments.extend(foreign_income_adj)
            
            # Loss carryforward
            loss_carryforward_adj = self._calculate_loss_carryforward_adjustments(df)
            adjustments.extend(loss_carryforward_adj)
            
            logger.info(f"Calculated {len(adjustments)} tax adjustments")
            
        except Exception as e:
            logger.error(f"Error calculating tax adjustments: {str(e)}")
            raise
        
        return adjustments
    
    def _calculate_depreciation_adjustments(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate depreciation adjustments"""
        adjustments = []
        
        try:
            # Look for depreciation columns
            depreciation_cols = [col for col in df.columns if 'depreciation' in col.lower()]
            
            for col in depreciation_cols:
                if col in df.columns and df[col].dtype in ['int64', 'float64']:
                    amount = df[col].sum()
                    if amount != 0:
                        adjustments.append({
                            'type': 'depreciation',
                            'category': TAX_ADJUSTMENTS['depreciation']['en'],
                            'description': TAX_ADJUSTMENTS['depreciation']['description'],
                            'amount': amount,
                            'source_column': col,
                            'adjustment_type': 'deduction'
                        })
        
        except Exception as e:
            logger.error(f"Error calculating depreciation adjustments: {str(e)}")
        
        return adjustments
    
    def _calculate_provisions_adjustments(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate provisions adjustments"""
        adjustments = []
        
        try:
            # Look for provisions columns
            provisions_cols = [col for col in df.columns if 'provision' in col.lower()]
            
            for col in provisions_cols:
                if col in df.columns and df[col].dtype in ['int64', 'float64']:
                    amount = df[col].sum()
                    if amount != 0:
                        adjustments.append({
                            'type': 'provisions',
                            'category': TAX_ADJUSTMENTS['provisions']['en'],
                            'description': TAX_ADJUSTMENTS['provisions']['description'],
                            'amount': amount,
                            'source_column': col,
                            'adjustment_type': 'deduction'
                        })
        
        except Exception as e:
            logger.error(f"Error calculating provisions adjustments: {str(e)}")
        
        return adjustments
    
    def _calculate_capital_gains_adjustments(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate capital gains adjustments"""
        adjustments = []
        
        try:
            # Look for capital gains columns
            capital_gains_cols = [col for col in df.columns if 'capital' in col.lower()]
            
            for col in capital_gains_cols:
                if col in df.columns and df[col].dtype in ['int64', 'float64']:
                    amount = df[col].sum()
                    if amount != 0:
                        adjustments.append({
                            'type': 'capital_gains',
                            'category': TAX_ADJUSTMENTS['capital_gains']['en'],
                            'description': TAX_ADJUSTMENTS['capital_gains']['description'],
                            'amount': amount,
                            'source_column': col,
                            'adjustment_type': 'income'
                        })
        
        except Exception as e:
            logger.error(f"Error calculating capital gains adjustments: {str(e)}")
        
        return adjustments
    
    def _calculate_foreign_income_adjustments(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate foreign income adjustments"""
        adjustments = []
        
        try:
            # Look for foreign income columns
            foreign_income_cols = [col for col in df.columns if 'foreign' in col.lower()]
            
            for col in foreign_income_cols:
                if col in df.columns and df[col].dtype in ['int64', 'float64']:
                    amount = df[col].sum()
                    if amount != 0:
                        adjustments.append({
                            'type': 'foreign_income',
                            'category': TAX_ADJUSTMENTS['foreign_income']['en'],
                            'description': TAX_ADJUSTMENTS['foreign_income']['description'],
                            'amount': amount,
                            'source_column': col,
                            'adjustment_type': 'income'
                        })
        
        except Exception as e:
            logger.error(f"Error calculating foreign income adjustments: {str(e)}")
        
        return adjustments
    
    def _calculate_loss_carryforward_adjustments(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate loss carryforward adjustments"""
        adjustments = []
        
        try:
            # Look for loss carryforward columns
            loss_carryforward_cols = [col for col in df.columns if 'loss' in col.lower()]
            
            for col in loss_carryforward_cols:
                if col in df.columns and df[col].dtype in ['int64', 'float64']:
                    amount = df[col].sum()
                    if amount != 0:
                        adjustments.append({
                            'type': 'loss_carryforward',
                            'category': TAX_ADJUSTMENTS['loss_carryforward']['en'],
                            'description': TAX_ADJUSTMENTS['loss_carryforward']['description'],
                            'amount': amount,
                            'source_column': col,
                            'adjustment_type': 'deduction'
                        })
        
        except Exception as e:
            logger.error(f"Error calculating loss carryforward adjustments: {str(e)}")
        
        return adjustments
    
    def calculate_tax_liability(self, net_income: float, adjustments: List[Dict]) -> Dict:
        """
        Calculate tax liability based on net income and adjustments
        Tax liability calculation based on net income and adjustments
        """
        try:
            # Calculate adjusted income
            total_adjustments = sum(adj['amount'] for adj in adjustments)
            adjusted_income = net_income + total_adjustments
            
            # Calculate tax
            tax_rate = self.tax_rates['corporate']
            tax_liability = adjusted_income * tax_rate
            
            return {
                'net_income': net_income,
                'total_adjustments': total_adjustments,
                'adjusted_income': adjusted_income,
                'tax_rate': tax_rate,
                'tax_liability': tax_liability,
                'effective_tax_rate': (tax_liability / net_income) if net_income != 0 else 0
            }
        
        except Exception as e:
            logger.error(f"Error calculating tax liability: {str(e)}")
            raise
    
    def get_tax_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get comprehensive tax summary
        Getting comprehensive tax summary
        """
        try:
            # Calculate all adjustments
            adjustments = self.calculate_adjustments(df)
            
            # Calculate net income (assuming it's in a specific column)
            net_income = 0
            income_cols = [col for col in df.columns if 'income' in col.lower()]
            if income_cols:
                net_income = df[income_cols[0]].sum()
            
            # Calculate tax liability
            tax_liability = self.calculate_tax_liability(net_income, adjustments)
            
            return {
                'net_income': net_income,
                'adjustments': adjustments,
                'tax_liability': tax_liability,
                'total_adjustments': len(adjustments),
                'adjustment_categories': list(set(adj['type'] for adj in adjustments))
            }
        
        except Exception as e:
            logger.error(f"Error getting tax summary: {str(e)}")
            raise
