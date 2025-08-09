import pandas as pd
import sys
import os

# Add the backend directory to the path
sys.path.append('backend')

from services.financial_analyzer import FinancialAnalyzer

# Read the Excel file
df = pd.read_excel('data/uploads/‏‏test4.xlsx')

print("Testing Enhanced FinancialAnalyzer")
print("=" * 50)

# Initialize analyzer
analyzer = FinancialAnalyzer(df)

# Perform analysis
result = analyzer.analyze("comprehensive")

# Display results
summary = result['summary']
print(f"Revenue: ₪{summary.get('revenue', 0):,.0f}")
print(f"Expenses: ₪{summary.get('expenses', 0):,.0f}")
print(f"Taxes: ₪{summary.get('taxes', 0):,.0f}")
print(f"Net Profit: ₪{summary.get('net_profit', 0):,.0f}")
print(f"Tax Rate: {summary.get('tax_rate', 0):.1f}%")
print(f"Profit Margin: {summary.get('profit_margin', 0):.1f}%")
print(f"Average ETR: {summary.get('average_etr', 0):.1f}%")
print(f"Jurisdictions: {summary.get('jurisdictions', 0)}")
print(f"Estimated Taxes: {summary.get('estimated_taxes', False)}")

print("\nRecommendations:")
recommendations = analyzer.generate_recommendations(result)
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

print("\n" + "="*60)
print("DETAILED CALCULATION EXPLANATIONS")
print("="*60)

# Display tax calculation explanation
if 'tax_calculation' in result.get('calculation_explanations', {}):
    tax_explanation = result['calculation_explanations']['tax_calculation']
    print(f"\n📊 TAX CALCULATION EXPLANATION:")
    print(f"Type: {tax_explanation['type'].upper()}")
    print(f"Method: {tax_explanation['method']}")
    print(f"Method (Hebrew): {tax_explanation.get('method_he', 'N/A')}")
    print(f"Formula: {tax_explanation['formula']}")
    print(f"Formula (Hebrew): {tax_explanation.get('formula_he', 'N/A')}")
    print(f"Result: {tax_explanation['result']}")
    print(f"Explanation: {tax_explanation['explanation']}")
    print(f"Explanation (Hebrew): {tax_explanation.get('explanation_he', 'N/A')}")

# Display ETR calculation explanation
if 'etr_calculation' in result.get('calculation_explanations', {}):
    etr_explanation = result['calculation_explanations']['etr_calculation']
    print(f"\n📈 ETR CALCULATION EXPLANATION:")
    print(f"Type: {etr_explanation['type'].upper()}")
    print(f"Method: {etr_explanation['method']}")
    print(f"Method (Hebrew): {etr_explanation.get('method_he', 'N/A')}")
    print(f"Formula: {etr_explanation['formula']}")
    print(f"Formula (Hebrew): {etr_explanation.get('formula_he', 'N/A')}")
    print(f"Result: {etr_explanation['result']}")
    print(f"Explanation: {etr_explanation['explanation']}")
    print(f"Explanation (Hebrew): {etr_explanation.get('explanation_he', 'N/A')}")
