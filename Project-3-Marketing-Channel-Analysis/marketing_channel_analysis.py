import pandas as pd
import os

# ============================================
# MARKETING CHANNEL ANALYSIS
# Google Analytics Sample Data — July 2017
# RaizoVision Portfolio Project
# ============================================


# Load datasets
summary = pd.read_csv('campaign_channel_performance.csv')
trends = pd.read_csv('ga_channel_daily_trends.csv')

# --- PART 1: CHANNEL PERFORMANCE SUMMARY ---


# Clean column names
summary.columns = summary.columns.str.strip().str.lower().str.replace(' ', '_')

# Fill null transactions and revenue with 0
summary['total_transactions'] = summary['total_transactions'].fillna(0)
summary['total_revenue'] = summary['total_revenue'].fillna(0)


# Calculate derived metrics
summary['conversion_rate'] = (
    summary['total_transactions'] / summary['total_sessions'] * 100
).round(2)

summary['revenue_per_session'] = (
    summary['total_revenue'] / summary['total_sessions']
).round(4)

summary['avg_revenue_per_transaction'] = summary.apply(
    lambda x: round(x['total_revenue'] / x['total_transactions'], 2)
    if x['total_transactions'] > 0 else 0, axis=1
)

# Sort by revenue
summary = summary.sort_values('total_revenue', ascending=False)

print("=== CHANNEL PERFORMANCE SUMMARY")
print(summary.to_string(index=False))
print(f"\nTotal channels analysed: {len(summary)}")
print(f"Total sessions: {summary['total_sessions'].sum():,}")
print(f"Total revenue: ${summary['total_revenue'].sum():,.2f}")


# --- PART 2: DAILY TRENDS ---

trends = pd.read_csv('ga_channel_daily_trends.csv')

# Clean column names
trends.columns = trends.columns.str.strip().str.lower().str.replace(' ', '_')

# Convert date
trends['session_date'] = pd.to_datetime(trends['session_date'])

# Fill nulls
trends['total_transactions'] = trends['total_transactions'].fillna(0)
trends['total_revenue'] = trends['total_revenue'].fillna(0)

# Calculate daily conversion rate
trends['conversion_rate'] = (
    trends['total_transactions'] / trends['total_sessions'] * 100
).round(2)

# Calculate 7-day rolling average revenue per channel
trends = trends.sort_values(['traffic_medium', 'session_date'])
trends['revenue_7day_avg'] = trends.groupby('traffic_medium')['total_revenue'].transform(
    lambda x: x.rolling(7, min_periods=1).mean()
).round(2)

print("\n=== DAILY TRENDS SAMPLE (first 10 rows) ===")
print(trends.head(10).to_string(index=False))

# --- PART 3: KEY INSIGHTS ---

print("\n=== KEY INSIGHTS ===")

# Top channel by revenue
top_revenue = summary.iloc[0]
print(
    f"Top channel by revenue: {top_revenue['traffic_medium']} — ${top_revenue['total_revenue']:,.2f}")

# Top channel by conversion rate (minimum 100 sessions)
top_conversion = summary[summary['total_sessions'] >= 100].sort_values(
    'conversion_rate', ascending=False
).iloc[0]
print(
    f"Best converting channel (100+ sessions): {top_conversion['traffic_medium']} — {top_conversion['conversion_rate']}%")

# Most efficient channel — revenue per session
top_efficiency = summary[summary['total_sessions'] >= 100].sort_values(
    'revenue_per_session', ascending=False
).iloc[0]
print(
    f"Most efficient channel (revenue/session): {top_efficiency['traffic_medium']} — ${top_efficiency['revenue_per_session']:.4f}")

# --- EXPORT FOR POWER BI ---

summary.to_csv('output_channel_summary.csv', index=False)
trends.to_csv('output_daily_trends.csv', index=False)

print("\n=== FILES EXPORTED FOR POWER BI ===")
print("output_channel_summary.csv")
print("output_daily_trends.csv")
print("\nProject complete.")
