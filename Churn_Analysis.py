import pandas as pd
import numpy as np

np.random.seed(77)
n = 1000

df = pd.DataFrame({
    'customer_id': range(2001, 2001 + n),
    'age': np.random.randint(18, 65, n),
    'gender': np.random.choice(['Male', 'Female'], n),
    'contract_type': np.random.choice(
        ['Monthly', 'Quarterly', 'Annual'], n,
        p=[0.5, 0.3, 0.2]),
    'monthly_spend': np.round(
        np.random.uniform(20, 200, n), 2),
    'tenure_months': np.random.randint(1, 60, n),
    'num_complaints': np.random.randint(0, 6, n),
    'last_login_days_ago': np.random.randint(1, 120, n),
    'num_products': np.random.randint(1, 5, n),
    'email_engagement': np.round(
        np.random.uniform(0, 1, n), 2),
    'support_calls': np.random.randint(0, 10, n),
})

# Create churn label based on realistic logic
# Normalize each factor to 0-1 range properly
complaints_score = df['num_complaints'] / 5
recency_score = df['last_login_days_ago'] / 120
disengagement_score = 1 - df['email_engagement']
support_score = df['support_calls'] / 10
contract_score = (df['contract_type'] == 'Monthly').astype(int) * 0.5
tenure_score = 1 - (df['tenure_months'] / 60)  # newer = higher risk

churn_probability = (
    complaints_score * 0.20 +
    recency_score * 0.25 +
    disengagement_score * 0.20 +
    support_score * 0.15 +
    contract_score * 0.10 +
    tenure_score * 0.10
)

# Use percentile-based threshold for exactly ~30% churn
threshold = np.percentile(churn_probability, 70)
df['churned'] = (churn_probability > threshold).astype(int)
df['churn_probability'] = churn_probability.round(3)

print(f"Dataset shape: {df.shape}")
print(f"\nChurn Rate: {df['churned'].mean()*100:.1f}%")
print(f"Churned customers: {df['churned'].sum()}")
print(f"Retained customers: {(df['churned']==0).sum()}")
print(f"Threshold used: {threshold:.3f}")
print("\nFirst 5 rows:")
print(df.head().to_string())


# ── Step 2: Churn Analysis ───────────────────────────────────────

print("\n=== CHURN BY CONTRACT TYPE ===")
contract_churn = df.groupby('contract_type').agg(
    total_customers=('customer_id', 'count'),
    churned=('churned', 'sum'),
    churn_rate=('churned', 'mean')
).round(3)
contract_churn['churn_rate_%'] = (
    contract_churn['churn_rate'] * 100).round(1)
print(contract_churn[['total_customers', 'churned', 'churn_rate_%']])

print("\n=== CHURN BY COMPLAINTS ===")
df['complaint_group'] = pd.cut(
    df['num_complaints'],
    bins=[-1, 0, 2, 5],
    labels=['No Complaints', '1-2 Complaints', '3+ Complaints'])
print(df.groupby('complaint_group')['churned'].mean().mul(100).round(1))

print("\n=== REVENUE AT RISK ===")
churned_revenue = df[df['churned']==1]['monthly_spend'].sum()
total_revenue = df['monthly_spend'].sum()
print(f"Monthly revenue at risk: ${churned_revenue:,.0f}")
print(f"Total monthly revenue:   ${total_revenue:,.0f}")
print(f"% revenue at risk:       {churned_revenue/total_revenue*100:.1f}%")

print("\n=== AVG PROFILE: CHURNED VS RETAINED ===")
profile = df.groupby('churned').agg(
    avg_tenure=('tenure_months', 'mean'),
    avg_spend=('monthly_spend', 'mean'),
    avg_complaints=('num_complaints', 'mean'),
    avg_last_login=('last_login_days_ago', 'mean'),
    avg_support_calls=('support_calls', 'mean'),
    avg_email_engagement=('email_engagement', 'mean')
).round(2)
profile.index = ['Retained', 'Churned']
print(profile)

# ── Export for Power BI ──────────────────────────────────────────
df.to_csv(
    r'C:\Users\as860\OneDrive\Desktop\Python\marketing\churn_analysis.csv',
    index=False)
print("\nFile saved! Ready for Power BI.")