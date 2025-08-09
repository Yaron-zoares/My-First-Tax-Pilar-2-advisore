import pandas as pd
from typing import Dict, List, Any, Union
import re
from datetime import datetime

class DataValidator:
    """
    Validates data for Pillar Two analysis with comprehensive error checking
    """
    
    def __init__(self):
        self.required_fields = {
            "financial_data": ["pre_tax_income", "current_tax_expense"],
            "entity_data": ["entity_name", "tax_residence"],
            "basic_financial": ["revenue", "profit_before_tax"]
        }
        
        self.field_types = {
            "pre_tax_income": (int, float),
            "current_tax_expense": (int, float),
            "deferred_tax_expense": (int, float),
            "revenue": (int, float),
            "entity_name": str,
            "tax_residence": str
        }
        
        self.validation_rules = {
            "pre_tax_income": {"min": 0, "max": float('inf')},
            "current_tax_expense": {"min": 0, "max": float('inf')},
            "revenue": {"min": 0, "max": float('inf')}
        }
    
    def validate_financial_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validates financial data and provides detailed error messages"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check required fields
        for field in self.required_fields["financial_data"]:
            if field not in data:
                errors.append(f"Missing required field: {field}")
                suggestions.append(f"Add {field} to the data")
            elif not isinstance(data[field], self.field_types.get(field, (int, float))):
                warnings.append(f"Field {field} should be numeric, got {type(data[field]).__name__}")
                suggestions.append(f"Convert {field} to numeric value")
        
        # Check for negative values
        for field in ["pre_tax_income", "current_tax_expense", "deferred_tax_expense"]:
            if field in data:
                if data[field] < 0:
                    warnings.append(f"Negative value in {field}: {data[field]}")
                    suggestions.append(f"Verify {field} calculation")
                elif data[field] == 0 and field == "pre_tax_income":
                    warnings.append(f"Zero pre_tax_income may cause calculation issues")
                    suggestions.append("Verify income calculations")
        
        # Check for reasonable values
        if "pre_tax_income" in data and "current_tax_expense" in data:
            if data["pre_tax_income"] > 0 and data["current_tax_expense"] > data["pre_tax_income"]:
                warnings.append("Tax expense exceeds pre-tax income")
                suggestions.append("Verify tax calculations")
        
        # Check for missing entity information
        for field in self.required_fields["entity_data"]:
            if field not in data:
                warnings.append(f"Missing entity field: {field}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "validated_data": data,
            "validation_timestamp": datetime.now().isoformat()
        }
    
    def validate_entity_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validates entity-specific data"""
        errors = []
        warnings = []
        
        # Check entity name format
        if "entity_name" in data:
            if not isinstance(data["entity_name"], str) or len(data["entity_name"].strip()) == 0:
                errors.append("Entity name must be a non-empty string")
        
        # Check tax residence format
        if "tax_residence" in data:
            if not isinstance(data["tax_residence"], str) or len(data["tax_residence"].strip()) == 0:
                errors.append("Tax residence must be a non-empty string")
        
        # Check jurisdiction codes
        if "jurisdictions" in data:
            if not isinstance(data["jurisdictions"], list):
                warnings.append("Jurisdictions should be a list")
            else:
                for jurisdiction in data["jurisdictions"]:
                    if not isinstance(jurisdiction, str):
                        warnings.append(f"Invalid jurisdiction format: {jurisdiction}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validated_data": data
        }
    
    def validate_excel_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validates Excel file structure for financial data"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("Excel file is empty")
            return {"is_valid": False, "errors": errors, "warnings": warnings}
        
        # Check for required columns (case-insensitive)
        required_columns = ["profit before tax", "current tax", "revenue"]
        found_columns = []
        
        for col in df.columns:
            col_lower = col.lower()
            if any(req in col_lower for req in required_columns):
                found_columns.append(col)
        
        missing_columns = [col for col in required_columns if not any(col in found.lower() for found in found_columns)]
        
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
            suggestions.append("Ensure Excel file contains: Profit Before Tax, Current Tax, Revenue")
        
        # Check for numeric columns
        for col in df.columns:
            if any(numeric_term in col.lower() for numeric_term in ["profit", "tax", "revenue", "income", "expense"]):
                if not pd.api.types.is_numeric_dtype(df[col]):
                    warnings.append(f"Column '{col}' should be numeric")
                    suggestions.append(f"Convert column '{col}' to numeric format")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "found_columns": found_columns,
            "total_columns": len(df.columns),
            "total_rows": len(df)
        }
    
    def validate_xml_structure(self, xml_content: str) -> Dict[str, Any]:
        """Validates XML structure for GIR reports"""
        errors = []
        warnings = []
        
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_content)
            
            # Check for required XML elements
            required_elements = ["Entity", "Name", "TaxResidence"]
            found_elements = []
            
            for elem in root.iter():
                if elem.tag in required_elements:
                    found_elements.append(elem.tag)
            
            missing_elements = [elem for elem in required_elements if elem not in found_elements]
            
            if missing_elements:
                errors.append(f"Missing required XML elements: {missing_elements}")
            
            # Check for proper XML structure
            if not root.tag.endswith("GIR"):
                warnings.append("Root element should be GIR")
            
        except ET.ParseError as e:
            errors.append(f"XML parsing error: {str(e)}")
        except Exception as e:
            errors.append(f"XML validation error: {str(e)}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
