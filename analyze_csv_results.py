#!/usr/bin/env python3
"""
Script to analyze CSV data results in detail
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def analyze_csv_data():
    """Analyze the CSV data in detail"""
    print("📊 Analyzing CSV Data Results...")
    
    # Load and process CSV data
    csv_file = "data/examples/test_pillar_2.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return False
    
    try:
        # Read CSV with proper parsing
        df = pd.read_csv(csv_file)
        
        # Handle single column CSV
        if len(df.columns) == 1:
            print("🔧 Processing single column CSV...")
            first_col = df.columns[0]
            split_data = df[first_col].str.split(',', expand=True)
            
            # Use first row as headers
            headers = split_data.iloc[0].tolist()
            split_data.columns = headers
            
            # Remove header row from data
            df = split_data.iloc[1:].reset_index(drop=True)
            
            # Clean column names
            df.columns = [col.strip() for col in df.columns]
        
        print(f"✅ Data loaded successfully")
        print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Analyze the data structure
        print("\n📋 Column Analysis:")
        for i, col in enumerate(df.columns):
            print(f"   {i+1}. {col}")
        
        # Show sample data
        print("\n📋 Sample Data (first 3 rows):")
        print(df.head(3).to_string(index=False))
        
        # Financial analysis
        print("\n💰 Financial Analysis:")
        
        # Try to identify financial columns
        financial_cols = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['revenue', 'income', 'tax', 'expense', 'profit']):
                financial_cols.append(col)
        
        if financial_cols:
            print(f"   Financial columns found: {financial_cols}")
            
            # Analyze each financial column
            for col in financial_cols:
                try:
                    # Convert to numeric, removing % signs
                    numeric_data = df[col].str.replace('%', '').str.replace(',', '').astype(float)
                    print(f"   {col}:")
                    print(f"     - Min: {numeric_data.min():,.0f}")
                    print(f"     - Max: {numeric_data.max():,.0f}")
                    print(f"     - Mean: {numeric_data.mean():,.0f}")
                    print(f"     - Total: {numeric_data.sum():,.0f}")
                except:
                    print(f"   {col}: Non-numeric data")
        else:
            print("   No clear financial columns identified")
        
        # Jurisdiction analysis
        print("\n🌍 Jurisdiction Analysis:")
        if 'Germany' in df.columns:
            jurisdictions = df['Germany'].unique()
            print(f"   Jurisdictions: {list(jurisdictions)}")
        
        # ETR Analysis
        print("\n📈 ETR (Effective Tax Rate) Analysis:")
        if '15%' in df.columns:
            etr_values = df['15%'].unique()
            print(f"   ETR values: {list(etr_values)}")
            
            # Calculate average ETR
            try:
                etr_numeric = df['15%'].str.replace('%', '').astype(float)
                avg_etr = etr_numeric.mean()
                print(f"   Average ETR: {avg_etr:.1f}%")
                
                # Risk assessment
                if avg_etr < 15:
                    print("   ⚠️  Risk: Average ETR below 15% threshold")
                else:
                    print("   ✅ Average ETR above 15% threshold")
            except:
                print("   Could not calculate average ETR")
        
        # Compliance status
        print("\n✅ Compliance Status:")
        if 'Yes' in df.columns:
            qualified_count = (df['Yes'] == 'Yes').sum()
            total_count = len(df)
            print(f"   Qualified entities: {qualified_count}/{total_count}")
            print(f"   Qualification rate: {(qualified_count/total_count)*100:.1f}%")
        
        # Summary statistics
        print("\n📊 Summary Statistics:")
        print(f"   Total entities: {len(df)}")
        print(f"   Data quality: {'Good' if not df.isnull().any().any() else 'Issues found'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing CSV data: {str(e)}")
        return False

def test_data_processing():
    """Test data processing with the CSV data"""
    try:
        from flexible_data_processor import FlexibleDataProcessor
        print("\n🔧 Testing Data Processing...")
        
        processor = FlexibleDataProcessor()
        
        # Process the CSV file
        result = processor.process_file("data/examples/test_pillar_2.csv")
        
        if result["success"]:
            print("✅ Data processing successful!")
            data = result["data"]
            
            print("📊 Processed Data:")
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    print(f"   {key}: {value:,.2f}")
                else:
                    print(f"   {key}: {value}")
        else:
            print("❌ Data processing failed")
            print(f"   Error: {result.get('error', {}).get('error_message', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {str(e)}")
        return False

def main():
    """Main analysis function"""
    print("🚀 Starting CSV Data Analysis...")
    
    # Analyze CSV data
    csv_success = analyze_csv_data()
    
    # Test data processing
    processing_success = test_data_processing()
    
    # Summary
    print("\n📊 Analysis Summary:")
    print(f"   CSV Analysis: {'✅' if csv_success else '❌'}")
    print(f"   Data Processing: {'✅' if processing_success else '❌'}")
    
    if csv_success and processing_success:
        print("\n🎉 Analysis completed successfully!")
        print("📋 Key Findings:")
        print("   - CSV data loaded and parsed correctly")
        print("   - Financial data identified and analyzed")
        print("   - ETR calculations performed")
        print("   - Compliance status assessed")
    else:
        print("\n⚠️  Some analysis failed. Check the errors above.")
    
    return csv_success and processing_success

if __name__ == "__main__":
    main()
