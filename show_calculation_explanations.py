import pandas as pd
import sys
import os

# Add the backend directory to the path
sys.path.append('backend')

from services.financial_analyzer import FinancialAnalyzer

def show_calculation_explanations(file_path):
    """Show detailed calculation explanations for a financial analysis"""
    
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    print("🔍 FINANCIAL ANALYSIS CALCULATION EXPLANATIONS")
    print("=" * 60)
    print(f"File: {file_path}")
    print(f"Data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = FinancialAnalyzer(df)
    
    # Perform analysis
    result = analyzer.analyze("comprehensive")
    
    # Display basic results
    summary = result['summary']
    print(f"\n📊 BASIC RESULTS:")
    print(f"Revenue: ₪{summary.get('revenue', 0):,.0f}")
    print(f"Expenses: ₪{summary.get('expenses', 0):,.0f}")
    print(f"Taxes: ₪{summary.get('taxes', 0):,.0f}")
    print(f"Net Profit: ₪{summary.get('net_profit', 0):,.0f}")
    print(f"Tax Rate: {summary.get('tax_rate', 0):.1f}%")
    print(f"Average ETR: {summary.get('average_etr', 0):.1f}%")
    
    # Display calculation explanations
    explanations = result.get('calculation_explanations', {})
    
    if not explanations:
        print("\n❌ No calculation explanations available")
        return
    
    print("\n" + "="*60)
    print("📋 DETAILED CALCULATION EXPLANATIONS")
    print("="*60)
    
    # Tax calculation explanation
    if 'tax_calculation' in explanations:
        tax_explanation = explanations['tax_calculation']
        print(f"\n💰 TAX CALCULATION:")
        print(f"   Type: {tax_explanation['type'].upper()}")
        print(f"   Method: {tax_explanation['method']}")
        print(f"   Method (Hebrew): {tax_explanation.get('method_he', 'N/A')}")
        print(f"   Formula: {tax_explanation['formula']}")
        print(f"   Formula (Hebrew): {tax_explanation.get('formula_he', 'N/A')}")
        print(f"   Result: {tax_explanation['result']}")
        print(f"   Explanation: {tax_explanation['explanation']}")
        print(f"   Explanation (Hebrew): {tax_explanation.get('explanation_he', 'N/A')}")
    
    # ETR calculation explanation
    if 'etr_calculation' in explanations:
        etr_explanation = explanations['etr_calculation']
        print(f"\n📈 ETR CALCULATION:")
        print(f"   Type: {etr_explanation['type'].upper()}")
        print(f"   Method: {etr_explanation['method']}")
        print(f"   Method (Hebrew): {etr_explanation.get('method_he', 'N/A')}")
        print(f"   Formula: {etr_explanation['formula']}")
        print(f"   Formula (Hebrew): {etr_explanation.get('formula_he', 'N/A')}")
        print(f"   Result: {etr_explanation['result']}")
        print(f"   Explanation: {etr_explanation['explanation']}")
        print(f"   Explanation (Hebrew): {etr_explanation.get('explanation_he', 'N/A')}")
    
    print("\n" + "="*60)
    print("✅ Analysis complete!")

if __name__ == "__main__":
    # Use the test file
    file_path = "data/uploads/‏‏test4.xlsx"
    show_calculation_explanations(file_path)
