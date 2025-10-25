# FLAVYR MVP - Restaurant Performance Diagnostic Platform

Phase 1 MVP: Benchmark comparison, gap analysis, and deal recommendations.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

FLAVYR now uses a streamlined, transaction-first workflow that provides both tactical and strategic insights from a single data upload.

### Step 1: Transaction Insights (Primary Entry Point)
1. Navigate to the "Transaction Insights" tab
2. Select your restaurant type (cuisine and dining model)
3. Upload your transaction-level CSV file (date, total, customer_id, item_name, day_of_week)
4. Click "Analyze Transactions & Generate Insights"
5. This triggers the complete pipeline:
   - Tactical analysis (slowest days, loyalty, AOV, item rankings)
   - Metric derivation (auto-calculates KPIs from transactions)
   - Benchmark comparison
   - Strategic recommendations

### Step 2: Dashboard
- View your performance grade (A-F)
- See 7 KPI comparisons vs industry benchmarks
- Analyze performance gaps with visual charts
- Metrics automatically derived from your transaction data

### Step 3: Recommendations
- Review prioritized business problems
- See recommended deal types ranked by severity
- Understand the rationale behind each recommendation
- Get both tactical and strategic improvement suggestions
- **NEW: Full Transparency Features**
  - "How Was This Calculated?" - Step-by-step calculation explanations
  - "Why This Severity?" - Visual severity scales with thresholds
  - "Confidence Details" - Data quality indicators with confidence scores
  - Data source badges showing exactly where insights came from

### Step 4: Export Report
- Generate downloadable PDF or HTML reports
- Share comprehensive performance insights with your team
- Includes both transaction insights and strategic analysis

For detailed usage instructions, see [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

## CSV Format

### Transaction-Level Data Format (Primary Input)

Upload transaction data with these required columns:

- `date` - Transaction date in YYYY-MM-DD format
- `total` - Transaction amount ($)
- `customer_id` - Unique customer identifier
- `item_name` - Item or product name
- `day_of_week` - Full day name (Monday, Tuesday, etc.)

**Sample file:** [data/sample_transaction_data.csv](data/sample_transaction_data.csv)

**What you get:**
- Tactical insights (slowest days, loyalty, AOV, item rankings)
- Auto-calculated strategic metrics (avg_ticket, covers, loyalty_rate)
- Benchmark comparison and performance grading
- Personalized deal recommendations

**Note:** Some metrics (labor_cost_pct, food_cost_pct, table_turnover, sales_per_sqft) cannot be derived from transaction data and will use industry defaults. Update these manually if you have actual data.

## Testing

Run the test script to validate functionality:

```bash
python test_app.py
```

## Project Structure

```
flavyr-mvp/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── data/                     # Sample data and benchmarks
│   ├── sample_restaurant_pos_data.csv
│   ├── sample_transaction_data.csv
│   ├── sample_industry_benchmark_data.csv
│   └── deal_bank_strategy_matrix.csv
├── database/                 # SQLite database (auto-created)
│   └── flavyr.db
├── src/                      # Core application logic
│   ├── data_loader.py        # Data loading and validation
│   ├── analyzer.py           # Performance gap analysis
│   ├── recommender.py        # Deal recommendations
│   ├── report_generator.py   # PDF/HTML reports
│   └── transaction_analyzer.py  # Transaction-level analytics
└── utils/                    # Helper functions
    ├── validators.py         # Data validation
    └── transaction_validator.py  # Transaction data validation
```

## Key Features

### Strategic Analytics
- CSV upload with validation
- Industry benchmark comparison (10 restaurant types)
- Performance gap analysis (7 KPIs)
- Deal recommendations mapped to business problems
- Interactive dashboard with charts
- Downloadable PDF and HTML reports

### Tactical Analytics (Transaction Insights)
- Transaction-level data analysis
- Slowest day identification (by transactions and revenue)
- Customer loyalty rate calculation
- Average order value by day of week
- Top/bottom selling items ranking
- Day-specific tactical recommendations

## Next Steps

After testing the MVP:
1. Pilot with 3-5 restaurants
2. Gather feedback on insights and recommendations
3. Iterate based on pilot results
4. Prepare for Phase 2 (Smart Clustering)

## Support

For issues or questions, refer to the planning documentation in `planning_docs/`.
