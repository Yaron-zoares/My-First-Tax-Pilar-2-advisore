"""
CSV Fixer Service
Handles malformed CSV files and converts them to proper format
"""

import pandas as pd
import re
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class CSVFixer:
    """Service to fix malformed CSV files"""
    
    @staticmethod
    def fix_malformed_csv(file_path: Path) -> Optional[pd.DataFrame]:
        """
        Fix malformed CSV file and return proper DataFrame
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Fixed DataFrame or None if fixing failed
        """
        try:
            # First try to read normally
            try:
                df = pd.read_csv(file_path)
                # Check if it's properly formatted (should have multiple columns)
                if len(df.columns) > 1:
                    logger.info(f"CSV file {file_path} is already properly formatted")
                    return df
            except Exception as e:
                logger.warning(f"Standard CSV reading failed: {str(e)}")
            
            # If we get here, the file is malformed
            logger.info(f"Attempting to fix malformed CSV: {file_path}")
            
            # Read the file as text first
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to fix the content
            fixed_content = CSVFixer._fix_csv_content(content)
            
            if fixed_content:
                # Create a temporary file with fixed content
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as temp_file:
                    temp_file.write(fixed_content)
                    temp_file_path = temp_file.name
                
                try:
                    # Read the fixed file
                    df = pd.read_csv(temp_file_path)
                    logger.info(f"Successfully fixed CSV file: {file_path}")
                    return df
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
            
            return None
            
        except Exception as e:
            logger.error(f"Error fixing CSV file {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def _fix_csv_content(content: str) -> Optional[str]:
        """
        Fix malformed CSV content
        
        Args:
            content: Raw CSV content as string
            
        Returns:
            Fixed CSV content or None if fixing failed
        """
        try:
            lines = content.strip().split('\n')
            if not lines:
                return None
            
            # Check if first line is malformed (contains quotes around entire line)
            first_line = lines[0].strip()
            
            # Pattern to detect malformed header
            if first_line.startswith('"') and first_line.endswith('"'):
                # Remove outer quotes and split by comma
                header_content = first_line[1:-1]  # Remove outer quotes
                headers = [h.strip() for h in header_content.split(',')]
                
                # Process data lines
                fixed_lines = [','.join(headers)]  # Add fixed header
                
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith('"') and line.endswith('"'):
                        # Remove outer quotes and split by comma
                        data_content = line[1:-1]
                        data_values = [v.strip() for v in data_content.split(',')]
                        fixed_lines.append(','.join(data_values))
                    else:
                        # Line is already properly formatted
                        fixed_lines.append(line)
                
                return '\n'.join(fixed_lines)
            
            return content
            
        except Exception as e:
            logger.error(f"Error fixing CSV content: {str(e)}")
            return None
    
    @staticmethod
    def detect_csv_issues(file_path: Path) -> Tuple[bool, str]:
        """
        Detect issues in CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Tuple of (has_issues, issue_description)
        """
        try:
            df = pd.read_csv(file_path)
            
            # Check for common issues
            issues = []
            
            if len(df.columns) == 1:
                issues.append("Single column detected - likely malformed headers")
            
            if df.empty:
                issues.append("Empty dataset")
            
            # Check for missing values in key columns
            key_columns = ['Revenue', 'GloBE Income', 'Covered Taxes']
            for col in key_columns:
                if col in df.columns:
                    missing_count = df[col].isna().sum()
                    if missing_count > 0:
                        issues.append(f"Missing values in {col}: {missing_count}")
            
            return len(issues) > 0, "; ".join(issues) if issues else "No issues detected"
            
        except Exception as e:
            return True, f"Error reading file: {str(e)}"
