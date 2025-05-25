import pandas as pd
import numpy as np

df = pd.read_csv("merged_data(1).csv")  # Load your data

cols_with_missing = ["MTS2VENTAS_NUM", "PUERTASREFRIG_NUM", "CAJONESESTACIONAMIENTO_NUM"]
df[cols_with_missing] = df[cols_with_missing].replace(0, np.nan)
from sklearn.impute import KNNImputer

knn_imputer = KNNImputer(n_neighbors=5)
df[cols_with_missing] = knn_imputer.fit_transform(df[cols_with_missing])

for col in cols_with_missing:
    df[f"{col}_was_missing"] = df[col].isna().astype(int)


# Save the cleaned DataFrame to a new CSV file
df.to_csv("knn.csv", index=False)  # Save the cleaned DataFrame to a new CSV file

