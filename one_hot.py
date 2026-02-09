import pandas as pd
import ast
from sklearn.preprocessing import MultiLabelBinarizer

# -----------------------------
# 1️⃣ Load your data
# -----------------------------
print("Loading data...")
df = pd.read_csv("patient_features.csv")

# -----------------------------
# 2️⃣ Convert string-lists into actual Python lists
# (VERY IMPORTANT if they are stored as strings like "['A','B']")
# -----------------------------
print("Converting string-lists to actual lists...")
list_cols = ['Cond', 'Proc', 'Med', 'Lab']

for col in list_cols:
    df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# -----------------------------
# 3️⃣ One-hot encode Gender & Ethnicity
# -----------------------------
print("One-hot encoding categorical columns...")
df = pd.get_dummies(df, columns=['gender', 'ethnicity'], prefix=['gender', 'eth'])

bool_cols = df.select_dtypes(include="bool").columns
df[bool_cols] = df[bool_cols].astype(int)

# -----------------------------
# 4️⃣ Multi-hot encode list columns
# -----------------------------
print("Multi-hot encoding list columns...")
for col in list_cols:
    mlb = MultiLabelBinarizer()
    
    encoded = mlb.fit_transform(df[col])
    
    encoded_df = pd.DataFrame(
        encoded,
        columns=[f"{col}_{cls}" for cls in mlb.classes_],
        index=df.index
    )
    
    df = pd.concat([df, encoded_df], axis=1)
    df.drop(columns=[col], inplace=True)

# -----------------------------
# 5️⃣ Done
# -----------------------------
print(df.shape)
print(df.head())

df.to_csv("encoded_data_hosp.csv.gz", index=False, compression="gzip")

df.to_csv("encoded_data_hosp.csv", index=False)

