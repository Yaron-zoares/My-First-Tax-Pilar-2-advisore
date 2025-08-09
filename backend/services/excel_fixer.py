"""
Excel Fixer Service
Handles malformed Excel files and converts them to proper format
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ExcelFixer:
    """Service to fix malformed Excel files"""
    
    @staticmethod
    def fix_malformed_excel(file_path: Path) -> Optional[pd.DataFrame]:
        """
        Fix malformed Excel file and return proper DataFrame
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Fixed DataFrame or None if fixing failed
        """
        try:
            logger.info(f"Attempting to fix Excel file: {file_path}")
            
            # Try to read the Excel file
            df = pd.read_excel(file_path)
            
            # Check if the file needs fixing
            if ExcelFixer._is_properly_formatted(df):
                logger.info(f"Excel file {file_path} is already properly formatted")
                return df
            
            # Fix the malformed Excel file
            fixed_df = ExcelFixer._fix_excel_content(df)
            
            if fixed_df is not None:
                logger.info(f"Successfully fixed Excel file: {file_path}")
                return fixed_df
            
            return None
            
        except Exception as e:
            logger.error(f"Error fixing Excel file {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def _is_properly_formatted(df: pd.DataFrame) -> bool:
        """
        Check if Excel DataFrame is properly formatted
        
        Args:
            df: DataFrame to check
            
        Returns:
            True if properly formatted, False otherwise
        """
        try:
            # Check if first row has meaningful column names (not Unnamed or NaN)
            first_row = df.iloc[0]
            unnamed_columns = [col for col in df.columns if 'Unnamed' in str(col)]
            
            # If more than 50% of columns are unnamed, it's malformed
            if len(unnamed_columns) > len(df.columns) * 0.5:
                return False
            
            # Check if first few rows contain NaN values (empty rows)
            first_few_rows = df.head(3)
            if first_few_rows.isna().all().all():
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"Error checking Excel format: {str(e)}")
            return False
    
    @staticmethod
    def _fix_excel_content(df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Fix malformed Excel content
        
        Args:
            df: Original DataFrame
            
        Returns:
            Fixed DataFrame or None if fixing failed
        """
        try:
            # Find the header row (row with meaningful column names)
            header_row_index = ExcelFixer._find_header_row(df)
            
            if header_row_index is None:
                logger.error("Could not find header row in Excel file")
                return None
            
            # Create new DataFrame with proper headers
            headers = df.iloc[header_row_index].tolist()
            
            # Clean up header names
            cleaned_headers = []
            for header in headers:
                if pd.isna(header):
                    cleaned_headers.append(f"Column_{len(cleaned_headers)}")
                else:
                    # Clean up the header name
                    header_str = str(header).strip()
                    if header_str == '':
                        cleaned_headers.append(f"Column_{len(cleaned_headers)}")
                    else:
                        cleaned_headers.append(header_str)
            
            # Get data rows (skip header row and any empty rows before it)
            data_rows = df.iloc[header_row_index + 1:].reset_index(drop=True)
            
            # Create new DataFrame with proper structure
            fixed_df = pd.DataFrame(data_rows.values, columns=cleaned_headers)
            
            # Remove any completely empty rows
            fixed_df = fixed_df.dropna(how='all')
            
            # Reset index
            fixed_df = fixed_df.reset_index(drop=True)
            
            logger.info(f"Fixed Excel file: {fixed_df.shape[0]} rows, {fixed_df.shape[1]} columns")
            logger.info(f"Headers: {list(fixed_df.columns)}")
            
            return fixed_df
            
        except Exception as e:
            logger.error(f"Error fixing Excel content: {str(e)}")
            return None
    
    @staticmethod
    def _find_header_row(df: pd.DataFrame) -> Optional[int]:
        """
        Find the row that contains the actual headers
        
        Args:
            df: DataFrame to search
            
        Returns:
            Index of header row or None if not found
        """
        try:
            # Look for common financial column names
            financial_keywords = [
                'jurisdiction', 'entity', 'revenue', 'income', 'tax', 'expense',
                'profit', 'margin', 'rate', 'amount', 'status', 'parent'
            ]
            
            # Check first 10 rows for headers
            for i in range(min(10, len(df))):
                row = df.iloc[i]
                
                # Convert row to string and check for financial keywords
                row_str = ' '.join([str(cell).lower() for cell in row if pd.notna(cell)])
                
                # Count how many financial keywords are found
                keyword_count = sum(1 for keyword in financial_keywords if keyword in row_str)
                
                # If we find at least 3 financial keywords, this is likely the header row
                if keyword_count >= 3:
                    logger.info(f"Found header row at index {i} with {keyword_count} financial keywords")
                    return i
            
            # If no financial keywords found, look for the first non-empty row
            for i in range(len(df)):
                row = df.iloc[i]
                if not row.isna().all():
                    # Check if this row has meaningful content (not just numbers)
                    non_numeric_count = 0
                    for cell in row:
                        if pd.notna(cell):
                            cell_str = str(cell)
                            if not cell_str.replace('.', '').replace('-', '').isdigit():
                                non_numeric_count += 1
                    
                    if non_numeric_count >= 2:  # At least 2 non-numeric values
                        logger.info(f"Found potential header row at index {i}")
                        return i
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding header row: {str(e)}")
            return None
    
    @staticmethod
    def detect_excel_issues(file_path: Path) -> Tuple[bool, str]:
        """
        Detect issues in Excel file
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Tuple of (has_issues, issue_description)
        """
        try:
            df = pd.read_excel(file_path)
            
            # Check for common issues
            issues = []
            
            # Check for unnamed columns
            unnamed_columns = [col for col in df.columns if 'Unnamed' in str(col)]
            if len(unnamed_columns) > len(df.columns) * 0.5:
                issues.append(f"Too many unnamed columns: {len(unnamed_columns)}/{len(df.columns)}")
            
            # Check for empty rows at the beginning
            first_few_rows = df.head(3)
            empty_rows = first_few_rows.isna().all(axis=1).sum()
            if empty_rows > 0:
                issues.append(f"Empty rows at beginning: {empty_rows}")
            
            # Check for missing values in key columns
            if not df.empty:
                # Look for potential financial columns
                potential_columns = [col for col in df.columns if any(keyword in str(col).lower() 
                                                                    for keyword in ['revenue', 'income', 'tax'])]
                for col in potential_columns:
                    missing_count = df[col].isna().sum()
                    if missing_count > 0:
                        issues.append(f"Missing values in {col}: {missing_count}")
            
            return len(issues) > 0, "; ".join(issues) if issues else "No issues detected"
            
        except Exception as e:
            return True, f"Error reading file: {str(e)}"
