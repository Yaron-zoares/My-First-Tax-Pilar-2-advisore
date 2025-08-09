import pandas as pd

# Read the Excel file
df = pd.read_excel('data/uploads/‏‏test4.xlsx')

print("Columns:", df.columns.tolist())
print("\nFull data:")
print(df.to_string())
print("\nSummary statistics:")
print(df.describe())

# Calculate potential tax values
print("\n=== Tax Analysis ===")
print("Revenue total:", df['Revenue ($)'].sum())
print("Total expenses:", df['HQ Expenses ($)'].sum() + df['Royalties (5%)'].sum() + df['Mgmt Fees ($)'].sum() + df['Consulting Fees ($)'].sum() + df['Interest (7% on $50M)'].sum())

# Calculate net income
revenue = df['Revenue ($)'].sum()
expenses = (df['HQ Expenses ($)'].sum() + df['Royalties (5%)'].sum() + 
           df['Mgmt Fees ($)'].sum() + df['Consulting Fees ($)'].sum() + 
           df['Interest (7% on $50M)'].sum())
net_income = revenue - expenses

print(f"Net income: {net_income:,.0f}")
print(f"Potential tax at 23%: {net_income * 0.23:,.0f}")
