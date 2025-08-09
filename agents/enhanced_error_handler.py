import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

class EnhancedErrorHandler:
    """
    Provides comprehensive error handling and analysis for Pillar Two data processing
    """
    
    def __init__(self):
        self.error_patterns = {
            "missing_data": [
                r"Missing required field",
                r"KeyError",
                r"IndexError.*out of range"
            ],
            "invalid_format": [
                r"Invalid format",
                r"JSONDecodeError",
                r"ParseError",
                r"Unsupported format"
            ],
            "calculation_error": [
                r"Calculation failed",
                r"Division by zero",
                r"TypeError.*unsupported operand",
                r"ValueError.*invalid literal"
            ],
            "file_error": [
                r"FileNotFoundError",
                r"PermissionError",
                r"OSError.*No such file"
            ],
            "data_validation_error": [
                r"Validation failed",
                r"Invalid data type",
                r"Required field missing"
            ]
        }
        
        self.error_suggestions = {
            "missing_data": [
                "Check if all required fields are provided in the input data",
                "Verify data format matches expected schema",
                "Ensure Excel/CSV files contain the required columns",
                "Check for typos in field names"
            ],
            "invalid_format": [
                "Verify the file format is supported (Excel, CSV, JSON, XML)",
                "Check if the file is corrupted or incomplete",
                "Ensure proper encoding (UTF-8 recommended)",
                "Try converting the file to a different format"
            ],
            "calculation_error": [
                "Verify numeric values are valid and not null",
                "Check for division by zero in calculations",
                "Ensure all required financial data is present",
                "Verify data types are correct (numeric vs text)"
            ],
            "file_error": [
                "Check if the file path is correct",
                "Verify file permissions and access rights",
                "Ensure the file exists and is not corrupted",
                "Try using absolute file paths"
            ],
            "data_validation_error": [
                "Review data validation rules and requirements",
                "Check for missing or invalid field values",
                "Verify data types match expected format",
                "Ensure all required fields are populated"
            ]
        }
        
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: str = "unknown") -> Dict[str, Any]:
        """Provides detailed error analysis and suggestions"""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "suggestions": [],
            "severity": "error",
            "timestamp": datetime.now().isoformat(),
            "error_category": self._categorize_error(error),
            "recovery_actions": []
        }
        
        # Categorize the error
        category = self._categorize_error(error)
        error_info["error_category"] = category
        
        # Add specific suggestions based on error category
        if category in self.error_suggestions:
            error_info["suggestions"] = self.error_suggestions[category]
        
        # Add recovery actions
        error_info["recovery_actions"] = self._get_recovery_actions(category, error)
        
        # Determine severity
        error_info["severity"] = self._determine_severity(category, error)
        
        # Log the error
        self.logger.error(f"Error in {context}: {error_info['error_type']} - {error_info['error_message']}")
        
        return error_info
    
    def _categorize_error(self, error: Exception) -> str:
        """Categorizes the error based on patterns"""
        error_message = str(error)
        
        for category, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    return category
        
        return "unknown_error"
    
    def _determine_severity(self, category: str, error: Exception) -> str:
        """Determines the severity level of the error"""
        critical_errors = ["calculation_error", "file_error"]
        warning_errors = ["data_validation_error"]
        
        if category in critical_errors:
            return "critical"
        elif category in warning_errors:
            return "warning"
        else:
            return "error"
    
    def _get_recovery_actions(self, category: str, error: Exception) -> List[str]:
        """Provides specific recovery actions based on error category"""
        recovery_actions = {
            "missing_data": [
                "Review input data structure",
                "Add missing required fields",
                "Check data source for completeness"
            ],
            "invalid_format": [
                "Convert file to supported format",
                "Check file encoding and structure",
                "Use data format adapter"
            ],
            "calculation_error": [
                "Validate input data types",
                "Check for null or invalid values",
                "Review calculation logic"
            ],
            "file_error": [
                "Verify file path and permissions",
                "Check file existence and integrity",
                "Try alternative file location"
            ],
            "data_validation_error": [
                "Review validation rules",
                "Fix data format issues",
                "Add missing required data"
            ]
        }
        
        return recovery_actions.get(category, ["Contact system administrator"])
    
    def validate_data_structure(self, data: Any, expected_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Validates data structure against expected format"""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "missing_fields": [],
            "extra_fields": [],
            "type_mismatches": []
        }
        
        if not isinstance(data, dict):
            validation_result["is_valid"] = False
            validation_result["errors"].append("Data must be a dictionary")
            return validation_result
        
        # Check for missing required fields
        for field, field_info in expected_structure.items():
            if field not in data:
                validation_result["missing_fields"].append(field)
                validation_result["is_valid"] = False
            else:
                # Check type compatibility
                expected_type = field_info.get("type", type(None))
                actual_type = type(data[field])
                
                if not isinstance(data[field], expected_type):
                    validation_result["type_mismatches"].append({
                        "field": field,
                        "expected": expected_type.__name__,
                        "actual": actual_type.__name__
                    })
                    validation_result["is_valid"] = False
        
        # Check for extra fields
        for field in data:
            if field not in expected_structure:
                validation_result["extra_fields"].append(field)
                validation_result["warnings"].append(f"Unexpected field: {field}")
        
        return validation_result
    
    def handle_validation_errors(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Handles validation errors and provides specific guidance"""
        error_info = {
            "validation_failed": not validation_result["is_valid"],
            "errors": validation_result["errors"],
            "warnings": validation_result["warnings"],
            "suggestions": [],
            "recovery_actions": []
        }
        
        if validation_result["missing_fields"]:
            error_info["suggestions"].append(f"Add missing fields: {', '.join(validation_result['missing_fields'])}")
            error_info["recovery_actions"].append("Review data source and add required fields")
        
        if validation_result["type_mismatches"]:
            for mismatch in validation_result["type_mismatches"]:
                error_info["suggestions"].append(
                    f"Convert field '{mismatch['field']}' from {mismatch['actual']} to {mismatch['expected']}"
                )
            error_info["recovery_actions"].append("Fix data type mismatches")
        
        if validation_result.get("extra_fields"):
            error_info["suggestions"].append(f"Consider removing extra fields: {', '.join(validation_result['extra_fields'])}")
        
        return error_info
    
    def create_error_report(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Creates a comprehensive error report"""
        if not errors:
            return {"status": "success", "message": "No errors found"}
        
        # Categorize errors
        error_categories = {}
        for error in errors:
            category = error.get("error_category", "unknown")
            if category not in error_categories:
                error_categories[category] = []
            error_categories[category].append(error)
        
        # Calculate statistics
        total_errors = len(errors)
        critical_errors = len([e for e in errors if e.get("severity") == "critical"])
        warnings = len([e for e in errors if e.get("severity") == "warning"])
        
        return {
            "status": "error" if critical_errors > 0 else "warning",
            "total_errors": total_errors,
            "critical_errors": critical_errors,
            "warnings": warnings,
            "error_categories": error_categories,
            "summary": {
                "most_common_category": max(error_categories.keys(), key=lambda k: len(error_categories[k])),
                "suggestions": self._get_common_suggestions(errors),
                "recovery_priority": self._get_recovery_priority(errors)
            }
        }
    
    def _get_common_suggestions(self, errors: List[Dict[str, Any]]) -> List[str]:
        """Extracts common suggestions from multiple errors"""
        all_suggestions = []
        for error in errors:
            all_suggestions.extend(error.get("suggestions", []))
        
        # Count frequency and return most common
        from collections import Counter
        suggestion_counts = Counter(all_suggestions)
        return [suggestion for suggestion, count in suggestion_counts.most_common(5)]
    
    def _get_recovery_priority(self, errors: List[Dict[str, Any]]) -> List[str]:
        """Determines recovery action priority"""
        critical_errors = [e for e in errors if e.get("severity") == "critical"]
        
        if critical_errors:
            return ["Fix critical errors first", "Validate data structure", "Check file formats"]
        else:
            return ["Review warnings", "Validate data quality", "Check for missing fields"]
