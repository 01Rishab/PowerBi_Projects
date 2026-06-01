import pandas as pd
import numpy as np

# ── LOAD ──────────────────────────────────────────────────
df = pd.read_csv("data/customer_shopping_behavior.csv", sep="\t")
print(f"Raw shape: {df.shape}")

# ── CLEAN COLUMN NAMES ────────────────────────────────────
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)
print("\nCleaned columns:", df.columns.tolist())

# ── FIX DATA TYPES ────────────────────────────────────────
bool_cols = ["subscription_status", "discount_applied", "promo_code_used"]
for col in bool_cols:
    df[col] = df[col].str.strip().str.title().map({"Yes": True, "No": False})

# ── HANDLE MISSING VALUES ─────────────────────────────────
median_rating = df["review_rating"].median()
df["review_rating"] = df["review_rating"].fillna(median_rating)
print(f"\nFilled review_rating nulls with median: {median_rating}")
print(f"Nulls remaining: {df.isnull().sum().sum()}")

# ── FEATURE ENGINEERING ───────────────────────────────────
bins   = [17, 25, 35, 45, 55, 70]
labels = ["18-25", "26-35", "36-45", "46-55", "56-70"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

def loyalty_tier(n):
    if n <= 10:  return "New"
    if n <= 25:  return "Regular"
    if n <= 40:  return "Loyal"
    return "Champion"

df["loyalty_tier"] = df["previous_purchases"].apply(loyalty_tier)
df["any_discount_used"] = df["discount_applied"] | df["promo_code_used"]
df["season_order"] = df["season"].map({"Spring":1, "Summer":2, "Fall":3, "Winter":4})

# ── VALIDATE ──────────────────────────────────────────────
assert df["review_rating"].isnull().sum() == 0, "Still has nulls!"
print(f"\nFinal shape: {df.shape}")
print(f"\nLoyalty tier counts:\n{df['loyalty_tier'].value_counts()}")

# ── CONVERT BOOLEANS TO 0/1 FOR POWER BI ─────────────────
# Must happen AFTER feature engineering since any_discount_used depends on them
df["subscription_status"] = df["subscription_status"].astype(int)
df["discount_applied"]     = df["discount_applied"].astype(int)
df["promo_code_used"]      = df["promo_code_used"].astype(int)
df["any_discount_used"]    = df["any_discount_used"].astype(int)

# ── EXPORT ────────────────────────────────────────────────
df.to_csv("data/cleaned_data.csv", index=False)
print("\n✅ Saved → data/cleaned_data.csv")




