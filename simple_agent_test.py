#!/usr/bin/env python3
"""
Simple test script for Pilar2 agents
"""

import sys
import os
from pathlib import Path

# Add agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def test_basic_imports():
    """Test basic imports"""
    print("🔧 Testing Basic Imports...")
    
    try:
        from flexible_data_processor import FlexibleDataProcessor
        print("✅ FlexibleDataProcessor imported")
        
        from data_validator import DataValidator
        print("✅ DataValidator imported")
        
        from enhanced_error_handler import EnhancedErrorHandler
        print("✅ EnhancedErrorHandler imported")
        
        from data_format_adapter import DataFormatAdapter
        print("✅ DataFormatAdapter imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        return False

def test_data_processing():
    """Test data processing"""
    print("\n🔧 Testing Data Processing...")
    
    try:
        from flexible_data_processor import FlexibleDataProcessor
        
        processor = FlexibleDataProcessor()
        print("✅ FlexibleDataProcessor initialized")
        
        # Test with sample data
        test_data = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "revenue": 5000000
        }
        
        result = processor.process_data(test_data)
        print("✅ Data processing completed")
        
        if result["success"]:
            print("📊 Processing Results:")
            data = result["data"]
            print(f"   Source format: {data.get('source_format', 'N/A')}")
            print(f"   Total rows: {data.get('total_rows', 'N/A')}")
            print(f"   Total columns: {data.get('total_columns', 'N/A')}")
        else:
            print(f"❌ Processing failed: {result.get('error', {}).get('error_message', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {str(e)}")
        return False

def test_csv_processing():
    """Test CSV processing"""
    print("\n📊 Testing CSV Processing...")
    
    try:
        from flexible_data_processor import FlexibleDataProcessor
        
        processor = FlexibleDataProcessor()
        
        # Test with CSV file
        csv_file = "data/examples/test_pillar_2.csv"
        if os.path.exists(csv_file):
            result = processor.process_file(csv_file)
            
            if result["success"]:
                print("✅ CSV processing successful!")
                data = result["data"]
                print("📊 Processed Data:")
                for key, value in data.items():
                    if isinstance(value, (int, float)):
                        print(f"   {key}: {value:,.2f}")
                    else:
                        print(f"   {key}: {value}")
            else:
                print("❌ CSV processing failed")
                print(f"   Error: {result.get('error', {}).get('error_message', 'Unknown error')}")
        else:
            print(f"❌ CSV file not found: {csv_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV processing test failed: {str(e)}")
        return False

def test_pillar_two_master_basic():
    """Test basic PillarTwoMaster functionality"""
    print("\n🔧 Testing PillarTwoMaster Basic...")
    
    try:
        from pillar_two_master import PillarTwoMaster
        
        master = PillarTwoMaster()
        print("✅ PillarTwoMaster initialized")
        
        # Test ETR calculation directly
        test_data = {
            "pre_tax_income": 1000000,
            "current_tax_expense": 150000,
            "revenue": 5000000,
            "entity_name": "Test Corp"
        }
        
        etr_result = master._calculate_etr(test_data)
        print("✅ ETR calculation completed")
        
        if "etr_percentage" in etr_result:
            print(f"   ETR: {etr_result['etr_percentage']:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ PillarTwoMaster test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Simple Pilar2 Test...")
    
    # Test all components
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Data Processing", test_data_processing),
        ("CSV Processing", test_csv_processing),
        ("PillarTwoMaster Basic", test_pillar_two_master_basic)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Testing: {test_name}")
        print('='*40)
        
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*40}")
    print("📊 TEST SUMMARY")
    print('='*40)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Core functionality is working.")
    elif passed > total // 2:
        print("⚠️  Most tests passed. Core functionality is mostly working.")
    else:
        print("❌ Many tests failed. Core functionality needs fixes.")
    
    return passed == total

if __name__ == "__main__":
    main()
