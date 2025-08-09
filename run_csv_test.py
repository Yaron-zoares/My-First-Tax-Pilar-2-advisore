#!/usr/bin/env python3
"""
Script to run and process CSV test files for Pilar2
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def run_csv_test(file_path: str):
    """Run CSV test file processing"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ Error: File not found: {file_path}")
            return False
        
        # Read CSV file
        print(f"📁 Reading CSV file: {file_path}")
        
        # Try different CSV parsing approaches
        try:
            # First try with default settings
            df = pd.read_csv(file_path)
        except:
            try:
                # Try with different separator
                df = pd.read_csv(file_path, sep=',')
            except:
                # Try with different encoding
                df = pd.read_csv(file_path, encoding='utf-8')
        
        # Check if data is in single column (comma-separated within quotes)
        if len(df.columns) == 1:
            print("🔧 Detected single column CSV, splitting data...")
            # Split the single column by commas
            first_col = df.columns[0]
            split_data = df[first_col].str.split(',', expand=True)
            
            # Use first row as headers
            headers = split_data.iloc[0].tolist()
            split_data.columns = headers
            
            # Remove the header row from data
            df = split_data.iloc[1:].reset_index(drop=True)
            
            # Clean up column names
            df.columns = [col.strip() for col in df.columns]
        
        print(f"✅ Successfully loaded CSV file")
        print(f"📊 Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Display first few rows
        print("\n📋 First 3 rows of data:")
        print(df.head(3).to_string(index=False))
        
        # Basic data analysis
        print("\n📈 Basic Data Analysis:")
        
        # Check for numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns
        if len(numeric_columns) > 0:
            print(f"💰 Numeric columns: {list(numeric_columns)}")
            print("\n📊 Summary statistics:")
            print(df[numeric_columns].describe())
        
        # Check for text columns
        text_columns = df.select_dtypes(include=['object']).columns
        if len(text_columns) > 0:
            print(f"\n📝 Text columns: {list(text_columns)}")
            for col in text_columns:
                unique_values = df[col].nunique()
                print(f"   {col}: {unique_values} unique values")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print(f"\n⚠️  Missing values:")
            for col, missing in missing_values.items():
                if missing > 0:
                    print(f"   {col}: {missing} missing values")
        else:
            print("\n✅ No missing values found")
        
        # Try to process with the data processor if available
        try:
            from flexible_data_processor import FlexibleDataProcessor
            print("\n🔧 Processing with FlexibleDataProcessor...")
            
            processor = FlexibleDataProcessor()
            result = processor.process_file(file_path)
            
            if result["success"]:
                print("✅ Data processing successful!")
                data = result["data"]
                print(f"📊 Processed data keys: {list(data.keys())}")
                
                # Show financial data if available
                financial_fields = ["pre_tax_income", "current_tax_expense", "revenue", "entity_name"]
                for field in financial_fields:
                    if field in data:
                        print(f"   {field}: {data[field]}")
            else:
                print("❌ Data processing failed:")
                print(f"   Error: {result.get('error', {}).get('error_message', 'Unknown error')}")
                
        except ImportError as e:
            print(f"⚠️  FlexibleDataProcessor not available, skipping advanced processing")
            print(f"   Import error: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing CSV file: {str(e)}")
        return False

def main():
    """Main function to run CSV test"""
    # Try different possible file names
    possible_files = [
        "data/examples/test_pillar_2.csv",
        "data/examples/pilar2_test_2.csv", 
        "data/examples/pillar2_test_dataset.csv"
    ]
    
    # Check which files exist
    existing_files = []
    for file_path in possible_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
    
    if not existing_files:
        print("❌ No CSV test files found!")
        print("Available files in data/examples/:")
        examples_dir = Path("data/examples")
        if examples_dir.exists():
            for file in examples_dir.glob("*.csv"):
                print(f"   - {file.name}")
        return False
    
    print("🔍 Found CSV test files:")
    for i, file_path in enumerate(existing_files, 1):
        print(f"   {i}. {file_path}")
    
    # Run test on first available file
    test_file = existing_files[0]
    print(f"\n🚀 Running test on: {test_file}")
    
    success = run_csv_test(test_file)
    
    if success:
        print("\n✅ CSV test completed successfully!")
        print("📊 Summary:")
        print("   - CSV file loaded successfully")
        print("   - Data structure analyzed")
        print("   - Basic validation completed")
    else:
        print("\n❌ CSV test failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()
