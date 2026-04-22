import pandas as pd
import numpy as np

# Set a seed so we get the same data every time
np.random.seed(42)

n = 1000

df = pd.DataFrame({
    'customer_id': range(1001, 1001 + n),
    'age': np.random.randint(18, 65, n),
    'gender': np.random.choice(['Male', 'Female'], n),
    'country': np.random.choice(['Hungary', 'Germany', 'France', 'Austria', 'Poland'], n, p=[0.4, 0.2, 0.15, 0.15, 0.1]),
    'total_spent': np.round(np.random.exponential(scale=250, size=n), 2),
    'num_purchases': np.random.randint(1, 30, n),
    'last_purchase_days_ago': np.random.randint(1, 365, n),
    'email_open_rate': np.round(np.random.uniform(0, 1, n), 2),
    'channel': np.random.choice(['Organic', 'Paid Social', 'Email', 'Referral'], n, p=[0.3, 0.3, 0.25, 0.15])
})

print(df.shape)
print(df.head())
print(df.describe())

# ── Step 2: Explore & Clean ──────────────────────────────────────

# 1. Check for missing values
print("=== Missing Values ===")
print(df.isnull().sum())

# 2. Check for duplicates
print(f"\n=== Duplicates: {df.duplicated().sum()} ===")

# 3. Spending distribution — are there any weird outliers?
print("\n=== Spending Stats ===")
print(f"Min spend:    ${df['total_spent'].min():.2f}")
print(f"Max spend:    ${df['total_spent'].max():.2f}")
print(f"Mean spend:   ${df['total_spent'].mean():.2f}")
print(f"Median spend: ${df['total_spent'].median():.2f}")

# 4. Channel breakdown — how are customers acquired?
print("\n=== Channel Distribution ===")
print(df['channel'].value_counts())

# 5. Gender breakdown
print("\n=== Gender Distribution ===")
print(df['gender'].value_counts())


# ── Step 3: Customer Segmentation ───────────────────────────────

# Define thresholds (based on median values — data-driven!)
spend_threshold = df['total_spent'].median()        # $171.53
recency_threshold = df['last_purchase_days_ago'].median()  # ~184 days

# Create segment labels


def assign_segment(row):
    high_spend = row['total_spent'] >= spend_threshold
    recent = row['last_purchase_days_ago'] <= recency_threshold

    if high_spend and recent:
        return 'Champion'
    elif high_spend and not recent:
        return 'At Risk'
    elif not high_spend and recent:
        return 'Potential'
    else:
        return 'Lost'


df['segment'] = df.apply(assign_segment, axis=1)

# ── Results ─────────────────────────────────────────────────────
print("=== Segment Distribution ===")
print(df['segment'].value_counts())

print("\n=== Average Stats per Segment ===")
summary = df.groupby('segment').agg(
    customers=('customer_id', 'count'),
    avg_spend=('total_spent', 'mean'),
    avg_purchases=('num_purchases', 'mean'),
    avg_days_since_purchase=('last_purchase_days_ago', 'mean'),
    avg_email_open_rate=('email_open_rate', 'mean')
).round(2)

print(summary)

# ── Export for Power BI ──────────────────────────────────────────
df.to_csv(r'C:\Users\as860\OneDrive\Desktop\Python\marketing\customers_segmented.csv', index=False)
print("\nFile saved! Ready for Power BI.")
