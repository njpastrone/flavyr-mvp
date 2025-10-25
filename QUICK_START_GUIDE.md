# FLAVYR Quick Start Guide

## New Data Pipeline

FLAVYR now uses a streamlined, transaction-first data pipeline that provides both tactical and strategic insights from a single data upload.

## Getting Started in 4 Steps

### Step 1: Navigate to Transaction Insights Tab

This is your starting point. The Transaction Insights tab is now the first tab after Home.

### Step 2: Provide Restaurant Information

Select your restaurant type:
- **Cuisine Type**: American, Italian, Mexican, Japanese, Vegetarian, Indian, Seafood, Mediterranean, or Asian Fusion
- **Dining Model**: Full Service, Casual Dining, Fast Casual, or Quick Service

### Step 3: Upload Transaction Data

Upload a CSV file with these required columns:
- `date` - Transaction date (YYYY-MM-DD)
- `total` - Transaction amount (numeric)
- `customer_id` - Customer identifier
- `item_name` - Item/product name
- `day_of_week` - Day name (Monday, Tuesday, etc.)

**Sample file available:** [data/sample_transaction_data.csv](data/sample_transaction_data.csv)

### Step 4: Run Analysis

Click **"Analyze Transactions & Generate Insights"** to:
1. Validate your data
2. Calculate tactical insights
3. Derive strategic metrics
4. Compare to industry benchmarks
5. Generate recommendations

## What You Get

### Tactical Insights (Transaction Insights Tab)
- **Slowest Days**: By transaction count and revenue
- **Customer Loyalty**: Repeat customer rate
- **Average Order Value**: Overall and by day
- **Top/Bottom Items**: Best and worst performers
- **Day-Specific Recommendations**: Actionable tactics

### Strategic Analysis (Dashboard Tab)
- **Performance Grade**: A-F rating vs. industry
- **7 KPI Comparisons**: Against benchmarks
- **Gap Visualization**: See where you stand
- **Derived Metrics**: Auto-calculated from transactions

### Deal Recommendations (Recommendations Tab)
- **Prioritized Issues**: Ranked by severity
- **Deal Suggestions**: Targeted promotions
- **Rationale**: Why each deal works
- **Critical vs. Standard Issues**: Organized by urgency

### Reports (Export Report Tab)
- **PDF Format**: For printing and sharing
- **HTML Format**: For web viewing
- **Complete Analysis**: All insights in one document

## How Metrics Are Derived

### From Transaction Data (High Confidence)
- **Average Ticket**: Mean of all transaction totals
- **Covers**: Average daily unique customers
- **Customer Repeat Rate**: % of customers with multiple transactions

### Industry Defaults (Update if you have actual data)
- **Labor Cost %**: 30% (industry average)
- **Food Cost %**: 30% (industry average)
- **Table Turnover**: 2.0x per service (industry average)
- **Sales per Sq Ft**: 100 (placeholder)

The pipeline uses these defaults to enable full analysis while maintaining accuracy where data is available.

## Data Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│ TRANSACTION INSIGHTS (Step 1)                               │
│ Upload: date, total, customer_id, item_name, day_of_week   │
└────────────────────────┬────────────────────────────────────┘
                        │
                        ▼
         ┌──────────────────────────────┐
         │ Tactical Analysis             │
         │ - Slowest days               │
         │ - Loyalty rate               │
         │ - AOV by day                 │
         │ - Item rankings              │
         └──────────┬───────────────────┘
                    │
                    ▼
         ┌──────────────────────────────┐
         │ Metric Derivation            │
         │ - Calculate avg_ticket       │
         │ - Calculate covers           │
         │ - Apply defaults             │
         └──────────┬───────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ DASHBOARD (Step 2)                                          │
│ Compare KPIs to Industry Benchmarks                         │
└────────────────────────┬────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ RECOMMENDATIONS (Step 3)                                     │
│ Get Personalized Deal Suggestions                           │
└────────────────────────┬────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ EXPORT REPORT (Step 4)                                      │
│ Download PDF or HTML Report                                 │
└─────────────────────────────────────────────────────────────┘
```

## Tips for Best Results

1. **Upload At Least 30 Days of Data**: More data = better insights
2. **Include Multiple Customers**: 10+ unique customers recommended
3. **Cover All Days of Week**: Essential for slowest day analysis
4. **Use Consistent Formats**: Follow the sample CSV structure
5. **Select Accurate Restaurant Type**: Ensures proper benchmark comparison

## Troubleshooting

### "No benchmark data found"
- Check that your cuisine type and dining model combination exists in the system
- Available combinations are shown in the dropdowns

### "Validation errors"
- Ensure all required columns are present
- Check date format (YYYY-MM-DD)
- Verify numeric values in 'total' column
- Use full day names (Monday, not Mon)

### "Only X transactions - recommend at least 30"
- This is a warning, not an error
- Analysis will still run but may be less accurate
- Upload more data for better insights

## Next Steps After Analysis

1. **Review Dashboard**: Understand your performance gaps
2. **Check Recommendations**: See suggested improvements
3. **Download Report**: Share with your team
4. **Implement Changes**: Apply tactical and strategic recommendations
5. **Re-analyze**: Upload new data to track improvements

## Need Help?

- Sample data: [data/sample_transaction_data.csv](data/sample_transaction_data.csv)
- Documentation: [DATA_PIPELINE_REORGANIZATION.md](DATA_PIPELINE_REORGANIZATION.md)
- Technical details: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
