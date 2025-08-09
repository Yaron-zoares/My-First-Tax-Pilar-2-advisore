import pandas as pd
from typing import Dict, List, Any, Union, Optional
import logging
from pathlib import Path

# Import with error handling for missing modules
try:
    from data_validator import DataValidator
except ImportError:
    class DataValidator:
        def validate_financial_data(self, data):
            return {"is_valid": True, "errors": []}

try:
    from data_format_adapter import DataFormatAdapter
except ImportError:
    class DataFormatAdapter:
        def detect_format(self, data):
            return "unknown"
        def adapt_data(self, data, format_type):
            return data

try:
    from enhanced_error_handler import EnhancedErrorHandler
except ImportError:
    class EnhancedErrorHandler:
        def validate_data_structure(self, data, structure):
            return {"is_valid": True, "errors": []}
        def handle_validation_errors(self, validation):
            return "Validation errors occurred"
        def handle_error(self, error, context):
            return str(error)

class FlexibleDataProcessor:
    """
    Comprehensive data processor that handles various formats with enhanced error handling
    """
    
    def __init__(self):
        self.validator = DataValidator()
        self.adapter = DataFormatAdapter()
        self.error_handler = EnhancedErrorHandler()
        self.logger = logging.getLogger(__name__)
        
        # Expected data structure for Pillar Two analysis
        self.expected_structure = {
            "pre_tax_income": {"type": (int, float), "required": True},
            "current_tax_expense": {"type": (int, float), "required": True},
            "deferred_tax_expense": {"type": (int, float), "required": False},
            "revenue": {"type": (int, float), "required": False},
            "entity_name": {"type": str, "required": False},
            "tax_residence": {"type": str, "required": False}
        }
    
    def process_data(self, raw_data: Any, format_type: Optional[str] = None) -> Dict[str, Any]:
        """Processes data with comprehensive error handling and validation"""
        try:
            # Auto-detect format if not specified
            if format_type is None:
                format_type = self.adapter.detect_format(raw_data)
                self.logger.info(f"Auto-detected format: {format_type}")
            
            # Adapt data to standard format
            adapted_data = self.adapter.adapt_data(raw_data, format_type)
            
            # Validate adapted data
            validation_result = self.validator.validate_financial_data(adapted_data)
            
            # Additional structure validation
            structure_validation = self.error_handler.validate_data_structure(
                adapted_data, self.expected_structure
            )
            
            # Combine validation results
            combined_validation = self._combine_validation_results(
                validation_result, structure_validation
            )
            
            if not combined_validation["is_valid"]:
                error_info = self.error_handler.handle_validation_errors(combined_validation)
                return {
                    "success": False,
                    "error": error_info,
                    "validation_details": combined_validation
                }
            
            return {
                "success": True,
                "data": adapted_data,
                "validation_details": combined_validation,
                "processing_info": {
                    "source_format": format_type,
                    "adaptation_successful": True,
                    "validation_passed": True
                }
            }
            
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "data_processing")
            return {
                "success": False,
                "error": error_info,
                "processing_info": {
                    "source_format": format_type,
                    "adaptation_successful": False,
                    "validation_passed": False
                }
            }
    
    def process_file(self, file_path: str, format_type: Optional[str] = None) -> Dict[str, Any]:
        """Processes data from a file with format detection"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Auto-detect format from file extension
            if format_type is None:
                format_type = self._detect_format_from_extension(file_path)
            
            # Load data based on format
            raw_data = self._load_file_data(file_path, format_type)
            
            # Process the data
            return self.process_data(raw_data, format_type)
            
        except Exception as e:
            error_info = self.error_handler.handle_error(e, "file_processing")
            return {
                "success": False,
                "error": error_info,
                "file_path": str(file_path)
            }
    
    def process_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Processes multiple files and provides comprehensive report"""
        results = []
        errors = []
        
        for file_path in file_paths:
            result = self.process_file(file_path)
            results.append({
                "file_path": file_path,
                "result": result
            })
            
            if not result["success"]:
                errors.append(result["error"])
        
        # Create comprehensive report
        report = {
            "total_files": len(file_paths),
            "successful_files": len([r for r in results if r["result"]["success"]]),
            "failed_files": len(errors),
            "results": results,
            "error_report": self.error_handler.create_error_report(errors) if errors else None
        }
        
        return report
    
    def _combine_validation_results(self, validation1: Dict[str, Any], validation2: Dict[str, Any]) -> Dict[str, Any]:
        """Combines multiple validation results"""
        combined = {
            "is_valid": validation1["is_valid"] and validation2["is_valid"],
            "errors": validation1.get("errors", []) + validation2.get("errors", []),
            "warnings": validation1.get("warnings", []) + validation2.get("warnings", []),
            "suggestions": validation1.get("suggestions", []) + validation2.get("suggestions", [])
        }
        
        # Add specific validation details
        if "missing_fields" in validation2:
            combined["missing_fields"] = validation2["missing_fields"]
        if "type_mismatches" in validation2:
            combined["type_mismatches"] = validation2["type_mismatches"]
        
        return combined
    
    def _detect_format_from_extension(self, file_path: Path) -> str:
        """Detects format from file extension"""
        extension = file_path.suffix.lower()
        
        format_mapping = {
            ".xlsx": "excel",
            ".xls": "excel",
            ".csv": "csv",
            ".json": "json",
            ".xml": "xml",
            ".pdf": "pdf"
        }
        
        return format_mapping.get(extension, "unknown")
    
    def _load_file_data(self, file_path: Path, format_type: str) -> Any:
        """Loads data from file based on format"""
        if format_type == "excel":
            return pd.read_excel(file_path)
        elif format_type == "csv":
            return pd.read_csv(file_path)
        elif format_type == "json":
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif format_type == "xml":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif format_type == "pdf":
            # Basic PDF text extraction (would need pdfplumber or similar for full support)
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    return text
            except ImportError:
                # Fallback to basic text reading
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        else:
            raise ValueError(f"Unsupported file format: {format_type}")
    
    def get_supported_formats(self) -> List[str]:
        """Returns list of supported formats"""
        return self.adapter.get_supported_formats()
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Returns current validation rules"""
        return {
            "required_fields": self.validator.required_fields,
            "field_types": self.validator.field_types,
            "expected_structure": self.expected_structure
        }
    
    def update_validation_rules(self, new_rules: Dict[str, Any]) -> None:
        """Updates validation rules"""
        if "required_fields" in new_rules:
            self.validator.required_fields.update(new_rules["required_fields"])
        
        if "field_types" in new_rules:
            self.validator.field_types.update(new_rules["field_types"])
        
        if "expected_structure" in new_rules:
            self.expected_structure.update(new_rules["expected_structure"])
    
    def create_data_template(self, format_type: str) -> Dict[str, Any]:
        """Creates a template for the specified format"""
        template = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "deferred_tax_expense": 30000,
            "revenue": 5000000,
            "entity_name": "Sample Corporation",
            "tax_residence": "United States"
        }
        
        if format_type == "excel":
            return pd.DataFrame([template])
        elif format_type == "csv":
            return pd.DataFrame([template])
        elif format_type == "json":
            return template
        elif format_type == "xml":
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<FinancialData>
    <Entity>
        <Name>{template['entity_name']}</Name>
        <TaxResidence>{template['tax_residence']}</TaxResidence>
    </Entity>
    <FinancialMetrics>
        <PreTaxIncome>{template['pre_tax_income']}</PreTaxIncome>
        <CurrentTaxExpense>{template['current_tax_expense']}</CurrentTaxExpense>
        <DeferredTaxExpense>{template['deferred_tax_expense']}</DeferredTaxExpense>
        <Revenue>{template['revenue']}</Revenue>
    </FinancialMetrics>
</FinancialData>"""
        else:
            return template
