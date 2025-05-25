import pandas as pd

# Load the existing data (already includes 'Meta_venta')
df = pd.read_csv('classified(3).csv')

# Ensure required columns exist
required_columns = ['AVG_VENTA_TOTAL', 'Meta_venta']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Create performance category based on ratio
def categorize_performance(row):
    ratio = row['AVG_VENTA_TOTAL'] / row['Meta_venta']
    if ratio >= 2.5:
        return 3  # Excellent
    elif ratio >= 1.75:
        return 2  # Meeting expectations
    else:
        return 1  # Below expectations

df['PERFORMANCE_CATEGORY'] = df.apply(categorize_performance, axis=1)

# Optional: Add human-readable labels
category_labels = {
    1: 'Below_Expectations',
    2: 'Meeting_Expectations',
    3: 'Excellent',
}
df['PERFORMANCE_LABEL'] = df['PERFORMANCE_CATEGORY'].map(category_labels)

# Save back to CSV
df.to_csv('classified(3).csv', index=False)
print("✅ Updated 'classified(3).csv' with PERFORMANCE_CATEGORY and PERFORMANCE_LABEL.")
