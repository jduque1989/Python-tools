import pandas as pd

# 1) Define your list of SKUs that should have '1' in the 4th column
new_sku = [
    "08007",
    "160013",
    "32244",
    "32163",
    "32093",
    "80073",
]

# 2) Read the original CSV
df = pd.read_csv("wc-product-export-31-3-2025-1743477757814.csv")

# ------------------------------------------------------------------------------
# Step 1: In the 4th column, change all '1' to '2'
# ------------------------------------------------------------------------------
df.iloc[:, 3] = df.iloc[:, 3].replace(1, 2)

# ------------------------------------------------------------------------------
# Step 2: For rows whose SKU is in new_sku, change the 4th column to '1'
# ------------------------------------------------------------------------------
# Assuming the SKU column in your CSV is named "SKU". Adjust if your SKU column
# has a different name (e.g., "sku", "Sku", etc.).
sku_column_name = "SKU"  # Update if needed

df.loc[df[sku_column_name].isin(new_sku), df.columns[3]] = 1

# ------------------------------------------------------------------------------
# Step 3: Erase (drop) all rows that have '0' in the 4th column
# ------------------------------------------------------------------------------
df = df[df.iloc[:, 3] != 0]

# ------------------------------------------------------------------------------
# Step 4: Change all remaining '2' in the 4th column to '0'
# ------------------------------------------------------------------------------
df.iloc[:, 3] = df.iloc[:, 3].replace(2, 0)

# ------------------------------------------------------------------------------
# Step 5: Export to new CSV file (keeping the same headers, no extra index column)
# ------------------------------------------------------------------------------
df.to_csv("modified_products.csv", index=False)
