import pandas as pd
import numpy as np

np.random.seed(99)

campaigns = pd.DataFrame({
    'campaign_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
    'campaign_name': [
        'Summer Sale Email',
        'Instagram Awareness',
        'Google Search Ads',
        'Referral Program',
        'Facebook Retargeting'
    ],
    'channel': ['Email', 'Instagram', 'Google', 'Referral', 'Facebook'],
    'budget_spent': [5000, 12000, 8500, 3000, 9500],
    'impressions': [85000, 420000, 95000, 15000, 310000],
    'clicks': [4200, 8800, 6200, 1800, 12400],
    'leads': [620, 480, 890, 310, 740],
    'customers_acquired': [198, 89, 312, 187, 203],
    'revenue_generated': [24500, 9800, 48200, 31600, 22100]
})

print(campaigns.to_string())

# ── Step 2: Calculate Marketing KPIs ────────────────────────────

# ROAS — how much revenue for every $1 spent
campaigns['ROAS'] = (campaigns['revenue_generated'] /
                     campaigns['budget_spent']).round(2)

# CAC — how much did each customer cost us
campaigns['CAC'] = (campaigns['budget_spent'] /
                    campaigns['customers_acquired']).round(2)

# Conversion Rate — what % of leads became customers
campaigns['conversion_rate_%'] = (
    (campaigns['customers_acquired'] / campaigns['leads']) * 100
).round(1)

# ROI — actual profit after subtracting spend
campaigns['ROI'] = (
    campaigns['revenue_generated'] - campaigns['budget_spent']
).round(2)

# ROI % — percentage return
campaigns['ROI_%'] = (
    ((campaigns['revenue_generated'] - campaigns['budget_spent']) /
     campaigns['budget_spent']) * 100
).round(1)

# Click Through Rate
campaigns['CTR_%'] = (
    (campaigns['clicks'] / campaigns['impressions']) * 100
).round(2)

# ── Step 3: Print Results ────────────────────────────────────────
print("=== CAMPAIGN KPI REPORT ===\n")

kpi_view = campaigns[[
    'campaign_name', 'budget_spent', 'revenue_generated',
    'ROAS', 'CAC', 'conversion_rate_%', 'ROI', 'ROI_%', 'CTR_%'
]]
print(kpi_view.to_string())

print("\n=== RANKINGS ===")
print(
    f"\nBest ROAS:       {campaigns.loc[campaigns['ROAS'].idxmax(), 'campaign_name']} ({campaigns['ROAS'].max()}x)")
print(
    f"Worst ROAS:      {campaigns.loc[campaigns['ROAS'].idxmin(), 'campaign_name']} ({campaigns['ROAS'].min()}x)")
print(
    f"Lowest CAC:      {campaigns.loc[campaigns['CAC'].idxmin(), 'campaign_name']} (${campaigns['CAC'].min()})")
print(
    f"Highest CAC:     {campaigns.loc[campaigns['CAC'].idxmax(), 'campaign_name']} (${campaigns['CAC'].max()})")
print(
    f"Best ROI%:       {campaigns.loc[campaigns['ROI_%'].idxmax(), 'campaign_name']} ({campaigns['ROI_%'].max()}%)")

# ── Export for Power BI ──────────────────────────────────────────
campaigns.to_csv(
    r'C:\Users\as860\OneDrive\Desktop\Python\marketing\campaigns_kpi.csv',
    index=False
)
print("\nFile saved! Ready for Power BI.")
