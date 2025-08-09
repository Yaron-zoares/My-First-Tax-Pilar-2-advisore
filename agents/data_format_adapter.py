import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Union
import re
from pathlib import Path
import logging

class DataFormatAdapter:
    """
    Adapts data from various formats to standard format for Pillar Two analysis
    """
    
    def __init__(self):
        self.adapters = {
            "excel": self._adapt_excel_data,
            "csv": self._adapt_csv_data,
            "xml": self._adapt_xml_data,
            "json": self._adapt_json_data,
            "pdf": self._adapt_pdf_data
        }
        
        # Column mapping for different formats
        self.column_mappings = {
            "excel": {
                "Profit Before Tax": "pre_tax_income",
                "Current Tax": "current_tax_expense",
                "Deferred Tax": "deferred_tax_expense",
                "Revenue": "revenue",
                "Tax Expense": "current_tax_expense",
                "Income Before Tax": "pre_tax_income",
                "Net Income": "net_income",
                "Total Revenue": "revenue"
            },
            "csv": {
                "profit_before_tax": "pre_tax_income",
                "current_tax": "current_tax_expense",
                "deferred_tax": "deferred_tax_expense",
                "revenue": "revenue",
                "tax_expense": "current_tax_expense",
                "income_before_tax": "pre_tax_income"
            }
        }
        
        self.logger = logging.getLogger(__name__)
    
    def adapt_data(self, data: Any, format_type: str) -> Dict[str, Any]:
        """Adapts data from various formats to standard format"""
        format_type = format_type.lower()
        
        if format_type not in self.adapters:
            raise ValueError(f"Unsupported format: {format_type}. Supported formats: {list(self.adapters.keys())}")
        
        try:
            return self.adapters[format_type](data)
        except Exception as e:
            self.logger.error(f"Error adapting {format_type} data: {str(e)}")
            raise
    
    def _adapt_excel_data(self, excel_data: pd.DataFrame) -> Dict[str, Any]:
        """Adapts Excel data to standard format"""
        adapted_data = {}
        
        # Map column names to standard format
        column_mapping = self.column_mappings["excel"]
        
        for excel_col in excel_data.columns:
            excel_col_lower = excel_col.lower()
            
            # Find matching standard column
            matched_col = None
            for pattern, standard_col in column_mapping.items():
                if pattern.lower() in excel_col_lower or excel_col_lower in pattern.lower():
                    matched_col = standard_col
                    break
            
            if matched_col:
                # Extract first non-null value
                value = excel_data[excel_col].dropna().iloc[0] if not excel_data[excel_col].dropna().empty else 0
                
                # Convert to numeric if possible
                try:
                    if isinstance(value, str):
                        # Remove currency symbols and commas
                        cleaned_value = re.sub(r'[^\d.-]', '', value)
                        value = float(cleaned_value) if cleaned_value else 0
                    adapted_data[matched_col] = value
                except (ValueError, TypeError):
                    adapted_data[matched_col] = 0
                    self.logger.warning(f"Could not convert column '{excel_col}' to numeric")
        
        # Add metadata
        adapted_data["source_format"] = "excel"
        adapted_data["total_rows"] = len(excel_data)
        adapted_data["total_columns"] = len(excel_data.columns)
        
        return adapted_data
    
    def _adapt_csv_data(self, csv_data: pd.DataFrame) -> Dict[str, Any]:
        """Adapts CSV data to standard format"""
        adapted_data = {}
        
        # Map column names to standard format
        column_mapping = self.column_mappings["csv"]
        
        for csv_col in csv_data.columns:
            csv_col_lower = csv_col.lower().replace(" ", "_")
            
            # Find matching standard column
            matched_col = None
            for pattern, standard_col in column_mapping.items():
                if pattern.lower() in csv_col_lower or csv_col_lower in pattern.lower():
                    matched_col = standard_col
                    break
            
            if matched_col:
                # Extract first non-null value
                value = csv_data[csv_col].dropna().iloc[0] if not csv_data[csv_col].dropna().empty else 0
                
                # Convert to numeric if possible
                try:
                    if isinstance(value, str):
                        # Remove currency symbols and commas
                        cleaned_value = re.sub(r'[^\d.-]', '', value)
                        value = float(cleaned_value) if cleaned_value else 0
                    adapted_data[matched_col] = value
                except (ValueError, TypeError):
                    adapted_data[matched_col] = 0
                    self.logger.warning(f"Could not convert column '{csv_col}' to numeric")
        
        # Add metadata
        adapted_data["source_format"] = "csv"
        adapted_data["total_rows"] = len(csv_data)
        adapted_data["total_columns"] = len(csv_data.columns)
        
        return adapted_data
    
    def _adapt_xml_data(self, xml_content: str) -> Dict[str, Any]:
        """Adapts XML data to standard format"""
        adapted_data = {}
        
        try:
            root = ET.fromstring(xml_content)
            
            # Extract financial data from XML
            for elem in root.iter():
                tag = elem.tag.lower()
                text = elem.text.strip() if elem.text else ""
                
                # Map XML elements to standard format
                if "profit" in tag and "tax" in tag:
                    adapted_data["pre_tax_income"] = self._parse_numeric(text)
                elif "tax" in tag and "expense" in tag:
                    adapted_data["current_tax_expense"] = self._parse_numeric(text)
                elif "deferred" in tag and "tax" in tag:
                    adapted_data["deferred_tax_expense"] = self._parse_numeric(text)
                elif "revenue" in tag:
                    adapted_data["revenue"] = self._parse_numeric(text)
                elif "entity" in tag and "name" in tag:
                    adapted_data["entity_name"] = text
                elif "tax" in tag and "residence" in tag:
                    adapted_data["tax_residence"] = text
            
            # Add metadata
            adapted_data["source_format"] = "xml"
            
        except ET.ParseError as e:
            self.logger.error(f"XML parsing error: {str(e)}")
            raise
        
        return adapted_data
    
    def _adapt_json_data(self, json_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Adapts JSON data to standard format"""
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON parsing error: {str(e)}")
                raise
        
        adapted_data = {}
        
        # Direct mapping for common JSON structures
        field_mapping = {
            "profit_before_tax": "pre_tax_income",
            "current_tax_expense": "current_tax_expense",
            "deferred_tax_expense": "deferred_tax_expense",
            "revenue": "revenue",
            "entity_name": "entity_name",
            "tax_residence": "tax_residence"
        }
        
        for json_field, standard_field in field_mapping.items():
            if json_field in json_data:
                value = json_data[json_field]
                if isinstance(value, (int, float)):
                    adapted_data[standard_field] = value
                elif isinstance(value, str):
                    # Try to parse numeric strings
                    try:
                        adapted_data[standard_field] = float(value)
                    except ValueError:
                        adapted_data[standard_field] = value
        
        # Add metadata
        adapted_data["source_format"] = "json"
        
        return adapted_data
    
    def _adapt_pdf_data(self, pdf_content: str) -> Dict[str, Any]:
        """Adapts PDF content to standard format using text extraction"""
        adapted_data = {}
        
        # Extract financial data using regex patterns
        patterns = {
            "pre_tax_income": r"(?:profit|income).*?(?:before|pre).*?tax.*?[\$€£]?\s*([\d,]+\.?\d*)",
            "current_tax_expense": r"(?:current|total).*?tax.*?expense.*?[\$€£]?\s*([\d,]+\.?\d*)",
            "revenue": r"(?:total|gross).*?revenue.*?[\$€£]?\s*([\d,]+\.?\d*)",
            "entity_name": r"(?:company|entity|corporation).*?name.*?:\s*([A-Za-z\s]+)",
            "tax_residence": r"(?:tax|fiscal).*?residence.*?:\s*([A-Za-z\s]+)"
        }
        
        for field, pattern in patterns.items():
            matches = re.findall(pattern, pdf_content, re.IGNORECASE)
            if matches:
                value = matches[0]
                if field in ["pre_tax_income", "current_tax_expense", "revenue"]:
                    # Convert to numeric
                    try:
                        cleaned_value = re.sub(r'[^\d.-]', '', value)
                        adapted_data[field] = float(cleaned_value) if cleaned_value else 0
                    except ValueError:
                        adapted_data[field] = 0
                else:
                    adapted_data[field] = value.strip()
        
        # Add metadata
        adapted_data["source_format"] = "pdf"
        adapted_data["content_length"] = len(pdf_content)
        
        return adapted_data
    
    def _parse_numeric(self, text: str) -> float:
        """Parse numeric value from text"""
        try:
            # Remove currency symbols and commas
            cleaned_text = re.sub(r'[^\d.-]', '', text)
            return float(cleaned_text) if cleaned_text else 0
        except ValueError:
            return 0
    
    def detect_format(self, data: Any) -> str:
        """Detects the format of the input data"""
        if isinstance(data, pd.DataFrame):
            return "excel" if "xlsx" in str(data) or "xls" in str(data) else "csv"
        elif isinstance(data, str):
            if data.strip().startswith("<?xml"):
                return "xml"
            elif data.strip().startswith("{"):
                return "json"
            else:
                return "pdf"  # Assume PDF content
        elif isinstance(data, dict):
            return "json"
        else:
            return "unknown"
    
    def get_supported_formats(self) -> List[str]:
        """Returns list of supported formats"""
        return list(self.adapters.keys())
