# Marketing Channel Performance Analysis (Project 4)

End-to-end marketing analytics project using Google BigQuery, Python, and Power BI to analyze channel performance from Google Analytics sample e-commerce data (July 2017).

## Project Overview

This project demonstrates a complete analytics workflow: extracting marketing data via SQL on BigQuery, processing and deriving metrics in Python with Pandas, and visualizing results in an interactive Power BI dashboard.

## Tools Used

- **Google BigQuery** — SQL queries on Google Analytics sample dataset
- **Python (Pandas)** — Data cleaning, derived metrics, trend analysis
- **Power BI** — Dashboard visualization and reporting

## Workflow

1. **SQL (BigQuery)** — Extracted channel performance summary and 31-day daily trend data from `bigquery-public-data.google_analytics_sample`
2. **Python (Pandas)** — Calculated conversion rate, revenue per session, average revenue per transaction, and 7-day rolling average revenue per channel
3. **Power BI** — Built a 4-visual dashboard: revenue by channel, daily revenue trend, conversion rate by channel, and key KPI cards

## Key Insights

- **Direct traffic ((none) medium) drives 99.9% of total revenue** ($8,292 of $8,304), indicating strong brand awareness but heavy dependence on a single channel with minimal contribution from paid acquisition channels.
- **July 5th shows an anomalous spike** — session volume jumped to 1,769 (5x the daily average) with revenue reaching $7,598 in a single day, suggesting a promotional event or external referral surge worth further investigation.
- **Conversion rate varies significantly day to day**, ranging from 0% to nearly 4%, highlighting an opportunity for consistent conversion rate optimization.
- **Peak conversion rate of 50%** (referral channel) reflects a single-channel anomaly with only 2 sessions — illustrating the importance of minimum sample size thresholds when interpreting channel-level conversion data.

## Files

- `marketing_channel_analysis.py` — Python processing script
- `output_channel_summary.csv` — Processed channel-level summary data
- `output_daily_trends.csv` — Processed daily trend data with rolling averages
- `marketing_channel_dashboard.pdf` — Power BI dashboard export

## Dashboard Preview

![Dashboard](marketing_channel_dashboard.pdf)

---
*Part of the RaizoVision portfolio — applying marketing analytics and consumer behaviour research to commercial decision-making.*
