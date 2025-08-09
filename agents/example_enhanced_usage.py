#!/usr/bin/env python3
"""
Example usage of the enhanced data processing system for Pillar Two analysis
"""

import json
import pandas as pd
from pathlib import Path

# Import the new data processing components
from flexible_data_processor import FlexibleDataProcessor
from data_validator import DataValidator
from enhanced_error_handler import EnhancedErrorHandler
from pillar_two_master import PillarTwoMaster

def example_1_basic_data_processing():
    """Example 1: Basic data processing with validation"""
    print("=== Example 1: Basic Data Processing ===")
    
    # Initialize the data processor
    processor = FlexibleDataProcessor()
    
    # Sample financial data
    sample_data = {
        "pre_tax_income": 1000000,
        "current_tax_expense": 150000,
        "deferred_tax_expense": 30000,
        "revenue": 5000000,
        "entity_name": "Sample Corporation",
        "tax_residence": "United States"
    }
    
    # Process the data
    result = processor.process_data(sample_data, "json")
    
    if result["success"]:
        print("✅ Data processing successful!")
        print(f"Source format: {result['processing_info']['source_format']}")
        print(f"Validation passed: {result['processing_info']['validation_passed']}")
        
        data = result["data"]
        print(f"Pre-tax income: €{data['pre_tax_income']:,.2f}")
        print(f"Current tax expense: €{data['current_tax_expense']:,.2f}")
        
        if result["validation_details"]["warnings"]:
            print(f"⚠️  Warnings: {', '.join(result['validation_details']['warnings'])}")
    else:
        print("❌ Data processing failed!")
        print(f"Error: {result['error']['error_message']}")
        if 'suggestions' in result['error']:
            print(f"Suggestions: {', '.join(result['error']['suggestions'])}")

def example_2_excel_file_processing():
    """Example 2: Processing Excel files with different column names"""
    print("\n=== Example 2: Excel File Processing ===")
    
    # Create sample Excel file with different column names
    sample_data = {
        "Profit Before Tax": [1000000],
        "Current Tax": [150000],
        "Revenue": [5000000],
        "Company Name": ["Sample Corp"]
    }
    
    df = pd.DataFrame(sample_data)
    excel_path = "sample_financial_data.xlsx"
    df.to_excel(excel_path, index=False)
    
    # Process the Excel file
    processor = FlexibleDataProcessor()
    result = processor.process_file(excel_path)
    
    if result["success"]:
        print("✅ Excel file processed successfully!")
        data = result["data"]
        print(f"Adapted pre-tax income: €{data['pre_tax_income']:,.2f}")
        print(f"Adapted current tax expense: €{data['current_tax_expense']:,.2f}")
        print(f"Source format: {data.get('source_format', 'unknown')}")
    else:
        print("❌ Excel processing failed!")
        print(f"Error: {result['error']['error_message']}")
    
    # Clean up
    Path(excel_path).unlink(missing_ok=True)

def example_3_error_handling():
    """Example 3: Comprehensive error handling"""
    print("\n=== Example 3: Error Handling ===")
    
    # Initialize error handler
    error_handler = EnhancedErrorHandler()
    
    # Test with invalid data
    invalid_data = {
        "pre_tax_income": -1000000,  # Negative value
        "current_tax_expense": "invalid",  # Wrong type
        # Missing required fields
    }
    
    # Validate the data
    validator = DataValidator()
    validation_result = validator.validate_financial_data(invalid_data)
    
    print("Validation Results:")
    print(f"Valid: {validation_result['is_valid']}")
    print(f"Errors: {validation_result['errors']}")
    print(f"Warnings: {validation_result['warnings']}")
    print(f"Suggestions: {validation_result['suggestions']}")
    
    # Handle validation errors
    error_info = error_handler.handle_validation_errors(validation_result)
    print(f"\nError Handling:")
    print(f"Suggestions: {error_info['suggestions']}")
    print(f"Recovery actions: {error_info['recovery_actions']}")

def example_4_multiple_formats():
    """Example 4: Processing multiple files in different formats"""
    print("\n=== Example 4: Multiple Format Processing ===")
    
    # Create sample files in different formats
    sample_data = {
        "pre_tax_income": 1000000,
        "current_tax_expense": 150000,
        "revenue": 5000000
    }
    
    # Create CSV file
    csv_data = pd.DataFrame([sample_data])
    csv_path = "sample_data.csv"
    csv_data.to_csv(csv_path, index=False)
    
    # Create JSON file
    json_path = "sample_data.json"
    with open(json_path, 'w') as f:
        json.dump(sample_data, f)
    
    # Process multiple files
    processor = FlexibleDataProcessor()
    file_paths = [csv_path, json_path]
    result = processor.process_multiple_files(file_paths)
    
    print(f"Multi-format processing results:")
    print(f"Total files: {result['total_files']}")
    print(f"Successful: {result['successful_files']}")
    print(f"Failed: {result['failed_files']}")
    
    if result.get('error_report'):
        print(f"Error report: {result['error_report']['status']}")
        if 'summary' in result['error_report']:
            print(f"Suggestions: {result['error_report']['summary']['suggestions']}")
    
    # Clean up
    Path(csv_path).unlink(missing_ok=True)
    Path(json_path).unlink(missing_ok=True)

def example_5_enhanced_pillar_two_analysis():
    """Example 5: Enhanced Pillar Two analysis with data processing"""
    print("\n=== Example 5: Enhanced Pillar Two Analysis ===")
    
    # Initialize Pillar Two Master
    master = PillarTwoMaster()
    
    # Sample financial data with potential issues
    financial_data = {
        "pre_tax_income": 1000000,
        "current_tax_expense": 120000,  # Below 15% threshold
        "deferred_tax_expense": 30000,
        "revenue": 5000000,
        "entity_name": "Test Corporation",
        "tax_residence": "Netherlands"
    }
    
    # Perform enhanced analysis
    result = master.analyze_pillar_two_compliance(financial_data)
    
    if "error" not in result:
        print("✅ Pillar Two analysis completed successfully!")
        
        # Display ETR analysis
        etr_analysis = result["etr_analysis"]
        print(f"ETR: {etr_analysis['etr_percentage']}%")
        print(f"Risk Level: {etr_analysis['risk_level']}")
        print(f"Risk Description: {etr_analysis['risk_description']}")
        
        # Display data quality assessment
        if "data_quality_assessment" in result:
            data_quality = result["data_quality_assessment"]
            print(f"Data Quality:")
            print(f"  Source format: {data_quality['source_format']}")
            print(f"  Validation passed: {data_quality['validation_passed']}")
            
            if data_quality.get('warnings'):
                print(f"  Warnings: {data_quality['warnings']}")
        
        # Display recommendations
        if result.get("recommendations"):
            print(f"\nRecommendations:")
            for rec in result["recommendations"]:
                print(f"  {rec['priority'].upper()}: {rec['description']}")
    else:
        print("❌ Pillar Two analysis failed!")
        print(f"Error: {result['error']}")
        if 'suggestions' in result:
            print(f"Suggestions: {result['suggestions']}")

def example_6_format_detection():
    """Example 6: Automatic format detection and processing"""
    print("\n=== Example 6: Format Detection ===")
    
    processor = FlexibleDataProcessor()
    
    # Test different data types
    test_cases = [
        # Excel DataFrame
        (pd.DataFrame({"Profit Before Tax": [1000000]}), "DataFrame"),
        # JSON string
        ('{"pre_tax_income": 1000000}', "JSON string"),
        # Dictionary
        ({"pre_tax_income": 1000000}, "Dictionary"),
        # XML string
        ('<?xml version="1.0"?><data><pre_tax_income>1000000</pre_tax_income></data>', "XML string")
    ]
    
    for data, description in test_cases:
        print(f"\nTesting {description}:")
        
        # Auto-detect format
        detected_format = processor.adapter.detect_format(data)
        print(f"  Detected format: {detected_format}")
        
        # Process data
        result = processor.process_data(data)
        if result["success"]:
            print(f"  ✅ Processing successful")
            print(f"  Source format: {result['data'].get('source_format', 'unknown')}")
        else:
            print(f"  ❌ Processing failed: {result['error']['error_message']}")

def example_7_validation_rules():
    """Example 7: Custom validation rules"""
    print("\n=== Example 7: Custom Validation Rules ===")
    
    processor = FlexibleDataProcessor()
    
    # Get current validation rules
    rules = processor.get_validation_rules()
    print("Current validation rules:")
    print(f"Required fields: {rules['required_fields']['financial_data']}")
    print(f"Field types: {list(rules['field_types'].keys())}")
    
    # Update validation rules
    new_rules = {
        "required_fields": {
            "financial_data": ["pre_tax_income", "current_tax_expense", "revenue"]
        },
        "field_types": {
            "revenue": (int, float)
        }
    }
    
    processor.update_validation_rules(new_rules)
    print("\nUpdated validation rules applied!")
    
    # Test with new rules
    test_data = {
        "pre_tax_income": 1000000,
        "current_tax_expense": 150000,
        "revenue": 5000000
    }
    
    result = processor.process_data(test_data)
    print(f"Validation with new rules: {'✅ Passed' if result['success'] else '❌ Failed'}")

def main():
    """Run all examples"""
    print("Enhanced Data Processing System - Examples")
    print("=" * 50)
    
    try:
        example_1_basic_data_processing()
        example_2_excel_file_processing()
        example_3_error_handling()
        example_4_multiple_formats()
        example_5_enhanced_pillar_two_analysis()
        example_6_format_detection()
        example_7_validation_rules()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        print("\nKey Benefits Demonstrated:")
        print("• Flexible data format support")
        print("• Comprehensive error handling")
        print("• Automatic format detection")
        print("• Enhanced validation")
        print("• Detailed error reporting")
        
    except Exception as e:
        print(f"❌ Example execution failed: {str(e)}")

if __name__ == "__main__":
    main()
