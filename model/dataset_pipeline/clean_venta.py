import pandas as pd

# Load your data
df = pd.read_csv("venta.csv")  # or use your DataFrame

def remove_outliers_iqr(group):
    Q1 = group["VENTA_TOTAL"].quantile(0.25)
    Q3 = group["VENTA_TOTAL"].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Return only rows within bounds
    return group[(group["VENTA_TOTAL"] >= lower_bound) & (group["VENTA_TOTAL"] <= upper_bound)]

# Apply per store
df_no_outliers = df.groupby("TIENDA_ID").apply(remove_outliers_iqr).reset_index(drop=True)

# Save the cleaned DataFrame to a new CSV file
# df_no_outliers.to_csv("venta_cleaned.csv", index=False)  # Save the cleaned DataFrame to a new CSV file

import matplotlib.pyplot as plt
import seaborn as sns

# Sample a few stores for clarity
sample_ids = df["TIENDA_ID"].drop_duplicates().sample(6, random_state=42)
df_sample = df[df["TIENDA_ID"].isin(sample_ids)]
df_clean_sample = df_no_outliers[df_no_outliers["TIENDA_ID"].isin(sample_ids)]

plt.figure(figsize=(14, 6))

# Before
plt.subplot(1, 2, 1)
sns.boxplot(x="TIENDA_ID", y="VENTA_TOTAL", data=df_sample)
plt.title("Before Removing Outliers")
plt.xticks(rotation=45)

# After
plt.subplot(1, 2, 2)
sns.boxplot(x="TIENDA_ID", y="VENTA_TOTAL", data=df_clean_sample)
plt.title("After Removing Outliers")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
